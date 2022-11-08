from google.cloud import pubsub_v1
from google.cloud import logging as gcloud_logging
import requests
import logging
import os

subscriber = pubsub_v1.SubscriberClient()
subscription_path = os.environ.get("SUBSCRIPTION_PATH")
api_url = os.environ.get("API_URL")

logging.basicConfig(level=logging.INFO)
logging_client = gcloud_logging.Client()
logging_client.setup_logging()


def request_api(pair, interval, start_date, end_date):
    url = f"{api_url}/api/v1/market-data/interval?start_date={start_date}&end_date={end_date}&pair={pair}&interval={interval}"

    response = requests.get(url)
    return response.text


def callback(message):
    if message.attributes:
        data = message.attributes
        pair = data.get("pair")
        interval = data.get("interval")
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        try:
            response = request_api(pair, interval, start_date, end_date)
            logging.info(response)
            message.ack()
        except Exception as e:
            logging.error(e)
            message.nack()


streaming_pull_future = subscriber.subscribe(
    subscription_path, callback=callback)
logging.info(f"Logging info message on... {subscription_path}")


# wrap subscriber in a 'with' block to automatically call close() when done
with subscriber:
    try:
        # streaming_pull_future.result(timeout=timeout)
        # going without a timeout will wait & block indefinitely
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()                          # trigger the shutdown
        # block until the shutdown is complete
        streaming_pull_future.result()
