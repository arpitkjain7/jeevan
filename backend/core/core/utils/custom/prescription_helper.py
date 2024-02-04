import io
from core.utils.aws.s3_helper import upload_to_s3
import os
import uuid
from pytz import timezone as pytz_timezone
from PIL import (
    Image,
)
from core import logger
import base64, json

logging = logger(__name__)
s3_location = os.environ["s3_location"]


def create_pdf_from_images(
    files,
):
    try:
        images = [Image.open(f) for f in files]
        pdf_buffer = io.BytesIO()
        images[0].save(
            pdf_buffer, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
        )
        pdf_buffer.seek(0)
        return pdf_buffer.read()
    except Exception as error:
        logging.error(f"Error in prepare_data function: {error}")
        raise error
