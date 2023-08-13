import boto3
from botocore.exceptions import ClientError
from core import logger
from botocore.config import Config
import json
import base64

logging = logger(__name__)
config = Config(signature_version="v4")
s3_client = boto3.client(
    "s3", config=config, endpoint_url="https://s3.ap-south-1.amazonaws.com"
)


def get_object(bucket_name: str, prefix: str):
    return s3_client.list_objects(Bucket=bucket_name, Prefix=prefix).get("Contents")


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client("s3")
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client("s3", region_name=region)
            location = {"LocationConstraint": region}
            s3_client.create_bucket(
                Bucket=bucket_name, CreateBucketConfiguration=location
            )
            s3_client.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    "BlockPublicAcls": True,
                    "IgnorePublicAcls": True,
                    "BlockPublicPolicy": True,
                    "RestrictPublicBuckets": True,
                },
            )
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_to_s3(bucket_name: str, byte_data: bytes, file_name: str):
    try:
        logging.info(f"Uploading file {file_name} to bucket {bucket_name}")
        _ = s3_client.put_object(
            ACL="private", Body=byte_data, Bucket=bucket_name, Key=file_name
        )
        return f"{bucket_name}/{file_name}"
    except ClientError as e:
        raise e


def create_presigned_url(bucket_name: str, key: str, expires_in: int):
    try:
        presigned_url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": key},
            ExpiresIn=expires_in,
        )
        return presigned_url
    except ClientError as e:
        logging.error(e)
        return None


def delete_s3(bucket_name: str, key: str):
    try:
        logging.info(f"Deleting file {key} from bucket {bucket_name}")
        _ = s3_client.delete_object(Bucket=bucket_name, Key=key)
        return True
    except ClientError as e:
        logging.error(e)
        return None


def read_object(bucket_name: str, prefix: str):
    response = s3_client.get_object(Bucket=bucket_name, Key=prefix)
    file_bytes = response["Body"].read()
    return base64.b64encode(file_bytes)
