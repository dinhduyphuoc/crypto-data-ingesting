from google.cloud import storage


def upload_to_storage(path: str, filename: str, data: str, dest_bucket_name: str):
    GCS_CLIENT = storage.Client()
    bucket = GCS_CLIENT.get_bucket(dest_bucket_name)
    blob = bucket.blob(path+filename)
    blob.upload_from_string(
        data,
        content_type='application/json'
    )
