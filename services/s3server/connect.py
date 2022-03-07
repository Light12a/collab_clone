import boto3
from utils.config import config

class S3Connection:
    client_s3 = None
    def __init__(self) -> None:
        """
        Connect to S3 Service
        """
        self.client_s3 = boto3.client(
            's3',
            aws_access_key_id = config['s3server']['access_key'],
            aws_secret_access_key = config['s3server']['secrect_access_key']
        )
        
    def upload_file(self):
        pass

    def download_file(self):
        pass