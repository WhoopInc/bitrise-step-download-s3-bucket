import boto3
from datetime import datetime
import logging
import os

class S3DownloadLogger(object):
    def __init__(self, file_size, filename):
        self._filename = filename
        self._size = file_size
        self._seen_so_far = 0
        self._seen_percentages = dict.fromkeys(list(range(0, 100, 10)), False)

    def __call__(self, bytes_amount):
        self._seen_so_far += bytes_amount
        percentage = round((self._seen_so_far / self._size) * 100)
        if percentage in self._seen_percentages.keys() and not self._seen_percentages[percentage]:
            self._seen_percentages[percentage] = True
            logging.info(f"Download progress at '{datetime.utcnow()}UTC: {percentage}%")

def initialize_resource(client_id, secret, region):
    s3_resource = boto3.resource('s3',
                             aws_access_key_id=client_id,
                             aws_secret_access_key=secret,
                             region_name=region
                             )
    return s3_resource

def download_file_from_s3(bucket, object, filename, s3_resource):
    file = s3_resource.Bucket(bucket).Object(object)
    logging.info(f"Starting download for '{file.key}'")
    download_logger = S3DownloadLogger(file.content_length, file.key)
    file.download_file(filename, Callback=download_logger)
    logging.info(f"Finished download for '{file.key}'")
    sys.exit(0)

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    ENV_VARS = ['client_id', 'secret', 'region', 'bucket', 'object', 'filename']
    for var in ENV_VARS:
        if var not in os.environ:
            raise EnvironmentError("{} is not set".format(var))
            sys.exit(1)
    s3_resource = initialize_resource(os.environ['client_id'], os.environ['secret'], os.environ['region'])
    download_file_from_s3(os.environ['bucket'], os.environ['object'], os.environ['filename'], s3_resource)