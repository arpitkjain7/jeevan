import pyqrcode
import png
from pyqrcode import QRCode
import os
import boto3
import io

s3 = boto3.resource("s3")


def qrcode_generator(event_uuid: str, event_bucket: str, event_name: str):
    bucket_obj = s3.Bucket(event_bucket)
    url = f"{os.environ['base_url']}{event_uuid}"
    url = pyqrcode.create(url)
    in_mem_file = io.BytesIO()
    url.png(in_mem_file, scale=6)
    in_mem_file.seek(0)
    bucket_obj.upload_fileobj(in_mem_file, f"{event_name}/metadata/qr.png")
    return {
        "qr_code_location": f"s3://{event_bucket}/{event_name}/metadata/qr.png",
        "s3_key": f"{event_name}/metadata/qr.png",
    }
