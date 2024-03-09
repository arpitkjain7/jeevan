from io import BytesIO
import io
from core.utils.aws.s3_helper import upload_bytes
from PyPDF2 import PdfMerger, PdfReader
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
        logging.info("executing create_pdf_from_images function")
        images = []
        for document in files:
            # logging.info(f"{document=}")
            image = Image.open(BytesIO(document))
            images.append(image)
        pdf_buffer = io.BytesIO()
        images[0].save(
            pdf_buffer, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
        )
        pdf_buffer.seek(0)
        return pdf_buffer.read()
    except Exception as error:
        logging.error(f"Error in create_pdf_from_images function: {error}")
        raise error


def merge_pdf(
    pdf1_bytes,
    files,
):
    try:
        logging.info("executing merge_pdf function")
        pdf2_bytes = create_pdf_from_images(files=files)
        #  logging.debug(f"{pdf2_bytes}")
        merger = PdfMerger()
        pdf1 = PdfReader(io.BytesIO(pdf1_bytes))
        merger.append(pdf1)
        pdf2 = PdfReader(io.BytesIO(pdf2_bytes))
        merger.append(pdf2)
        output_buffer = io.BytesIO()
        merger.write(output_buffer)
        merged_pdf = output_buffer.getvalue()

        return merged_pdf
    except Exception as error:
        logging.error(f"Error in merge_pdf function: {error}")
        raise error
