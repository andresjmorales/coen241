import os
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'cred.json'
storage_client = storage.Client()

def upload(bl_nm, file_name, bucket_nm):
    try:
        bucket = storage_client.get_bucket(bucket_nm)
        blob = bucket.blob(bl_nm)
        with open(file_name, "rb") as my_file:
            blob.upload_from_file(my_file)
        return True
    except Exception as e:
        print(e)
        return False
