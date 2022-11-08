from flask import Blueprint, jsonify, request
from multiprocessing import Process, Manager
from datetime import datetime
from pathlib import Path
from configparser import ConfigParser
from common.constants import *
from common.pairs import pairs
from utils.upload import upload_to_storage
from utils.redis import setInterval
from utils.utilities import *
import numpy as np
import time
import json
import pytz

# Class parameters


class PastParams:
    start_date = ""
    end_date = ""

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date


# Configuration
root = Path(__file__).parents[2]

config = ConfigParser()
config.read(f"{root}/config/config.ini")

# Define API endpoint prefix
market_module = Blueprint('market_module', __name__,
                          url_prefix='/api/v1/market-data')

# Checking valid query strings before request


@market_module.before_request
def validate_query_parameters():
    args = request.args
    interval = args.get("interval")
    if (interval not in MARKET_DATA.INTERVALS):
        return jsonify({"message": "Invalid interval",
                        "status": STATUS.HTTP_400_BAD_REQUEST}), STATUS.HTTP_400_BAD_REQUEST


@market_module.get("/interval")
def get_interval():
    args = request.args
    interval = args.get("interval")
    pairs = args.getlist("pair")
    start_date, end_date = args.get("start_date"), args.get("end_date")
    past = PastParams(start_date, end_date) if (
        start_date and end_date) else None

    try:
        data = get_pairs_interval_ohlcv(
            pairs, interval, past=past)
    except Exception as e:
        return jsonify(
            {"error": str(e),
             "status": STATUS.HTTP_500_INTERNAL_SERVER_ERROR}), STATUS.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        if (data is not None):
            return jsonify(data)
        else:
            raise Exception("3rd party API error")


def setRetryInterval(second, start_time, interval):

    current = time.time() - start_time
    while (current > second):
        setInterval(start_time, current, interval)
        current -= second


def get_isoformat8601(unix_timestamp):
    unix_timestamp = str(unix_timestamp)
    # tz = pytz.timezone('Asia/Saigon')
    try:
        if len(unix_timestamp) == 13:
            unix_timestamp = int(unix_timestamp[0:-3])
            return datetime.fromtimestamp(
                int(unix_timestamp)).replace(second=0, microsecond=0).isoformat()
        else:
            return datetime.fromtimestamp(
                int(unix_timestamp)).replace(second=0, microsecond=0).isoformat()
    except:
        return False


def get_ohlcv(pairs, start_date, end_date, interval):
    arr = []
    ohlcv_list = []
    # Extract pairs
    for i in pairs:
        for key, value in i.items():
            arr.append({key: value})

    # Extract OHLCV from raw json
    for i in arr:
        for key, value in i.items():
            open = value[0][1]
            high = max([value[i][2] for i in range(len(value))])
            low = min([value[i][3] for i in range(len(value))])
            close = value[len(value) - 1][4]
            volume = sum([value[i][5] for i in range(len(value))])

            ohlcv = {
                "pair": key,
                "start_date": start_date,
                "end_date": end_date,
                "interval": interval,
                "open": open,
                "high": high,
                "low": low,
                "close": close,
                "volume": round(volume, 2),
            }

            data = json.dumps(ohlcv)

            try:
                dir_struct = f"{key}/{end_date}/"
                file_name = f"{interval}.json"
                bucket_name = config.get("GCLOUD", "BUCKET_NAME")
                upload_to_storage(dir_struct, file_name,
                                  data, bucket_name)
            except Exception as e:
                print("Error: ", e)

            ohlcv_list.append(ohlcv)

    return ohlcv_list


def get_pairs_interval_ohlcv(data_pairs, interval, past=None, retry=False):
    start = time.time()

    print(f"Getting data in {interval}")

    # Get time length and interval
    time_length = int(interval[:-1])
    it = MARKET_DATA.INTERVAL_INITIAL[interval[-1]]

    if (past is None):
        now = get_isoformat8601(get_current_time_millisec())
        past = get_isoformat8601(
            now - (time_length * MARKET_DATA.INTERVAL_LENGTH[it] * TIME.MS))
    else:
        now = past.end_date
        past = past.start_date

    # Empty result array
    result = []

    # Split pairs to smaller chunks with <divided> pairs per chunk
    pairs_count = len(data_pairs)
    divided = (pairs_count //
               MARKET_DATA.PAIRS_PER_CALL) if pairs_count >= MARKET_DATA.PAIRS_PER_CALL else 1

    pairs_chunked = np.array_split(data_pairs, divided)

    # Setting up multiprocessing tasks
    start1 = time.time()
    with Manager() as manager:
        L = manager.list()
        processes = []
        for pair in pairs_chunked:
            p = Process(target=get_pair, args=(
                pair, past, now, it, L))
            p.start()
            processes.append(p)

        # If 1 request is failed as exit(1), add to retry queue or return NULL
        for p in processes:
            if p.exitcode == 1:
                if not retry:
                    setInterval(past, now, interval)
                return None
            p.join()

        result = list(L)

    print(f"Time taken for getting ohlcv in {interval}:", time.time() - start1)

    start2 = time.time()
    ohlcv = get_ohlcv(result, past, now, interval)

    now = time.time()
    print(
        f"Time taken for uploading to cloud storage in {interval}:", now - start2)

    setRetryInterval(
        MARKET_DATA.INTERVAL_LENGTH[it] * TIME.MS, start, interval)
    return ohlcv


def get_pair(pairs, past, now, it, L: list):
    try:
        parsed = ",".join(pairs)
        data = get_amber_coin_batch_historical(parsed, past, now, it)
    except Exception as e:
        print(e)
        exit(1)
    else:
        match data["status"]:
            case 200:
                L.append(data["payload"]["data"])
            case 404:
                raise Exception("Not Found")
            case 400:
                raise Exception("Bad request")
            case 500:
                raise Exception("Internal server error")
