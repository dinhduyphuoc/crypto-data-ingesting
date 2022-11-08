from configparser import ConfigParser

config = ConfigParser()

config["SETTINGS"] = {
    "X_API_KEY": "UAK35f99ed677591113f21d9df242cf5e2b"
}

config["GCLOUD"] = {
    "SCHEDULER_NAME": "projects/fresher-training-02/locations/us-central1/jobs/crypto",
    "SCHEDULER_PARENT": "projects/fresher-training-02/locations/us-central1",
    "SCHEDULER_URL": "http://35.209.228.22/api/v1/market-data/interval?interval",
    "SCHEDULER_RETRY_URL": "http://35.209.228.22/api/v1/retry-data/retry-error-api",
    "BUCKET_NAME": "crypto-data-test"
}

with open("config.ini", "w") as f:
    config.write(f)
