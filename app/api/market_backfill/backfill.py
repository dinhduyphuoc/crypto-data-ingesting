from flask import Blueprint, request
from datetime import datetime
from pathlib import Path
from configparser import ConfigParser
from google.cloud import pubsub_v1
from api.market.market import get_pairs_interval_ohlcv, get_pair, PastParams, get_isoformat8601
from common.constants import *
from common.pairs import pairs
from utils.utilities import *
import pandas as pd

# Configuration
root = Path(__file__).parents[2]

config = ConfigParser()
config.read(f"{root}/config/config.ini")

# Define API endpoint prefix
backfill_module = Blueprint(
    'market_module', __name__, url_prefix='/api/v1/market-data')

# Default parameters
param = {
    "m": "min",
    "h": "H",
    "d": "D"
}

freq = ["5min", "15min", "30min", "1H", "3H", "1D"]
freq_map = {"5min": "5m", "15min": "15m",
            "30min": "30m", "1H": "1h", "3H": "3h", "1D": "1d"}

# Setup publisher
publisher = pubsub_v1.PublisherClient()
topic_path = "projects/fresher-training-02/topics/crypto"


# @backfill_module.before_request
# def validate_datetime_difference():
#     args = request.args
#     start, end, interval = args.get(
#         "start_date"), args.get("end_date"), args.get("interval")

#     start_date, end_date, it = get_date_time(
#         int(start)), get_date_time(int(end)), interval[-1]

#     s, e = pd.to_datetime(start_date), pd.to_datetime(end_date)
#     difference = (e - s).total_seconds()

#     err_msg = """This endpoint returns a max of:
#                 1 month of daily data,
#                 1 days of hourly data,
#                 and 1 hour of minutely data"""

#     if ((
#         it == "m" and difference > TIME.HOUR) or (
#             it == "h" and difference > TIME.DAY) or (
#                 it == "d" and difference > TIME.MONTH)):
#         return jsonify({"error": err_msg,
#                         "status": STATUS.HTTP_400_BAD_REQUEST}), STATUS.HTTP_400_BAD_REQUEST


@ backfill_module.get("/history")
def get_history_intervals():
    args = request.args
    start_date, end_date, interval = args.get(
        'start_date'), args.get('end_date'), args.get('interval')

    df = pd.DataFrame(columns=freq)
    print(start_date, end_date)

    for f in freq:
        if freq_map[f] == interval:
            df[f] = pd.Series(pd.date_range(start_date, end_date, freq=f))
            df[f] = df[f].map(lambda x: datetime.strftime(
                x, '%Y-%m-%dT%H:%M:%SZ') if not pd.isnull(x) else x)

            for date in range(len(df[f]) - 1):
                if not pd.isnull(df[f][date + 1]):
                    for pair in pairs:
                        attributes = {
                            "pair": pair,
                            "interval": freq_map[f],
                            "start_date": df[f][date],
                            "end_date": df[f][date + 1]
                        }

                        data = "publish ohlcv"
                        data = data.encode("utf-8")

                        future = publisher.publish(
                            topic_path, data, **attributes)
                        print("Message ID: ", future.result())
                        print("Data: ", pair, freq_map[f],
                              df[f][date], df[f][date + 1])

    return "Done"
