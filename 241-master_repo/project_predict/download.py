import os
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'cred.json'
storage_client = storage.Client()

def download(bl_nm, file_name, bucket_nm):
    try:
        bucket = storage_client.get_bucket(bucket_nm)
        blob = bucket.blob(bl_nm)
        with open(file_name, "wb") as f:
            storage_client.download_blob_to_file(blob, f)
        return True
    except Exception as e:
        print(e)
        return False
