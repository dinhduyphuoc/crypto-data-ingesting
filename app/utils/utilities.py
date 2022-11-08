from configparser import ConfigParser
from datetime import datetime
from pathlib import Path
from common.constants import *
import requests
import time
import json

# Configuration
root = Path(__file__).parents[1]

config = ConfigParser()
config.read(f"{root}/config/config.ini")


def get_current_time_millisec():
    return int(time.time() * 1000)


def get_date_time(ms):
    return datetime.fromtimestamp(ms / 1000).isoformat()


def get_top_pairs():
    try:
        top_coins = get_amber_top_coins(
            "desc", "marketCap", MARKET_DATA.TOP_COINS)
    except:
        return json.loads(
            {"message": "Cannot get data from Amberdata"}), STATUS.HTTP_500_INTERNAL_SERVER_ERROR

    coins = []
    for coin in top_coins["payload"]["data"]:
        coins.append((coin["blockchain"]["symbol"]).lower())

    # get coin pairs
    stable_coins = ["_busd", "_usdt", "_usdc"]

    pairs = []
    for coin in coins:
        for stable_coin in stable_coins:
            pairs.append(f"{coin}{stable_coin}")

    return pairs


def get_amber_coin_batch_historical(pairs, start_date, end_date, interval):
    url = "https://web3api.io/api/v2/market/spot/ohlcv/exchange/binance/historical"

    querystring = {"pair": f"{pairs}", "startDate": f"{start_date}",
                   "endDate": f"{end_date}", "timeInterval": f"{interval}", "timeFormat": "human_readable"}

    headers = {
        "Accept": "application/json",
        "x-api-key": config.get("SETTINGS", "X_API_KEY")
    }

    response = requests.get(url, headers=headers,
                            params=querystring)

    return json.loads(response.text)


def get_amber_top_coins(direction, sortType, size, format="json"):
    url = "https://web3api.io/api/v2/market/rankings/latest"

    querystring = {"direction": f"{direction}",
                   "sortType": f"{sortType}", "size": f"{size}", "format": f"{format}"}

    headers = {
        "Accept": "application/json",
        "x-api-key": config.get("SETTINGS", "X_API_KEY")
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    return json.loads(response.text)
