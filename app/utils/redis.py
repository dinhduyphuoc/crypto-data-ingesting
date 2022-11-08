import redis
import json

r = redis.Redis(
    host='redis',
    port='6379')


def setInterval(start, end, interval):
    try:
        value = {
            "start": start,
            "end": end,
            "interval": interval
        }
        r.rpush('retry', json.dumps(value))
        return True
    except:
        return False


def getInterval():
    try:
        value = r.lpop('retry', 1)
        return json.loads(value[0].decode('UTF-8'))
    except:
        return None


def rollbackInterval(value):
    try:
        r.lpush('retry', json.dumps(value))
        return True
    except:
        return False


def swapInterval(value):
    try:
        r.rpush('retry', json.dumps(value))
        return True

    except:
        return None
