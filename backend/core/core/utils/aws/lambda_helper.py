import boto3
import os
from core import logger
import json

logging = logger(__name__)
lambda_client = boto3.client("lambda")


def invoke_thumbnail_creation(bucket_name: str, s3_key: str):
    try:
        lambda_function_name = os.environ.get("thumbnail_creation_lambda")
        lambda_client.invoke(
            FunctionName=lambda_function_name,
            InvocationType="Event",
            Payload=json.dumps({"bucket_name": bucket_name, "s3_key": s3_key}),
        )
    except Exception as error:
        logging.error(f"Error in  invoke_thumbnail_creation: {error}")
        raise error
