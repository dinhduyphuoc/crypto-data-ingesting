from flask import Blueprint
from api.market.market import get_pairs_interval_ohlcv, PastParams
from utils.redis import getInterval, swapInterval
from common.pairs import pairs
from common.constants import STATUS


# Define API endpoint prefix
retry_module = Blueprint('retry_module', __name__,
                         url_prefix='/api/v1/retry-data')


@retry_module.get('/retry-error-api')
def retryErrorApi():
    input = getInterval()

    if input is None:
        return 'empty content', STATUS.HTTP_204_NO_CONTENT

    try:
        start_date, end_date, interval = input["start"],
        input["end"],
        input["interval"]

        past = PastParams(start_date, end_date)

        result = get_pairs_interval_ohlcv(
            pairs, interval, past=past, retry=True)

        if result is not None:
            return 'success', STATUS.HTTP_200_OK
        else:
            swapInterval(input)

            return 'retry error', STATUS.HTTP_500_INTERNAL_SERVER_ERROR
    except:
        return 'retry error', STATUS.HTTP_500_INTERNAL_SERVER_ERROR
