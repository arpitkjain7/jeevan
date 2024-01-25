import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
import json
import base64

config = Config(signature_version="v4")
s3_client = boto3.client(
    "s3", config=config, endpoint_url="https://s3.ap-south-1.amazonaws.com"
)


def read_json(bucket_name: str, prefix: str):
    response = s3_client.get_object(Bucket=bucket_name, Key=prefix)
    json_data = response["Body"].read().decode("utf-8")
    data = json.loads(json_data)
    return data
