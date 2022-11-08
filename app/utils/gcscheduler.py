from datetime import timedelta
from google.cloud import scheduler
from configparser import ConfigParser
from pathlib import Path

# Configuration
root = Path(__file__).parents[1]

config = ConfigParser()
config.read(f"{root}/config/config.ini")


name = config.get("GCLOUD", "SCHEDULER_NAME")
parent = config.get("GCLOUD", "SCHEDULER_PARENT")
url = config.get("GCLOUD", "SCHEDULER_URL")
retry = config.get("GCLOUD", "SCHEDULER_RETRY_URL")


class IntervalSchedule:
    interval = ''
    schedule = ''

    def __init__(self, setinverval, setschedule):
        self.interval = setinverval
        self.schedule = setschedule


def get_job(jobname):
    client = scheduler.CloudSchedulerClient()
    return client.get_job(name=jobname)


def delete_job(jobname):
    client = scheduler.CloudSchedulerClient()
    client.delete_job(name=jobname)


def create_job(jobname, uri, schedule):
    # Create a client
    client = scheduler.CloudSchedulerClient()
   # parent = client.location_path("fresher-training-02",'us-central1')
    job = {
        "name": jobname,
        "http_target": {
            "http_method": "GET",
            "uri": uri,
            #  "headers": {"Content-Type": "application/json"},
            # "body": json.dumps(body).encode("utf-8"),
        },
        "schedule": schedule,
        # "attempt_deadline": timedelta(min),
    }

    # Make the request
#    response = client.create_job(parent,job)
    client.create_job(
        request={
            "parent": parent,
            "job": job
        }
    )


def createScheduler():

    interval = [IntervalSchedule('1m', '* * * * *'), IntervalSchedule('5m', '*/5 * * * *'), IntervalSchedule('15m', '*/15 * * * *'), IntervalSchedule(
        '30m', '*/30 * * * *'), IntervalSchedule('1h', '0 * * * *'), IntervalSchedule('3h', '0 */3 * * *'), IntervalSchedule('1d', '0 0 * * *')]

    for i in interval:
        try:
            get_job(f"{name}-{i.interval}")
        except:
            create_job(f"{name}-{i.interval}",
                       f"{url}={i.interval}", i.schedule)
            print('Creating scheduler ',i.interval)

    try:
        get_job(f"{name}-retry")
    except:
        create_job(f"{name}-retry",
                   f"{retry}", '* * * * *')


# resource "google_cloud_scheduler_job" "job" {
#   name             = "test-job"
#   description      = "test http job"
#   schedule         = "*/8 * * * *"
#   time_zone        = "America/New_York"
#   attempt_deadline = "320s"
#   retry_config {
#     retry_count = 1
#   }
#   http_target {
#     http_method = "POST"
#     uri         = "https://example.com/ping"
#     body        = base64encode("{\"foo\":\"bar\"}")
#   }
# }
