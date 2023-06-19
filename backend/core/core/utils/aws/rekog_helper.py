import boto3
from core import logger

client = boto3.client("rekognition")
logging = logger(__name__)


def compare_faces(sourceFileKey, targetFileKey):
    try:
        logging.info("compare_faces triggered")
        logging.info(f"compare_faces {sourceFileKey=}")
        logging.info(f"compare_faces {targetFileKey=}")
        source_bucket = sourceFileKey.split("//")[1].split("/")[0]
        target_bucket = targetFileKey.split("//")[1].split("/")[0]
        source_key = "/".join(sourceFileKey.split("//")[1].split("/")[1:])
        target_key = "/".join(targetFileKey.split("//")[1].split("/")[1:])
        response = client.compare_faces(
            SimilarityThreshold=90,
            SourceImage={"S3Object": {"Bucket": source_bucket, "Name": source_key}},
            TargetImage={"S3Object": {"Bucket": target_bucket, "Name": target_key}},
        )
        return response["FaceMatches"]
    except Exception as error:
        logging.error(f"Error in compare_faces function: {error}")
        return []
