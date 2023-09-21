import pyqrcode
import io


def qrcode_generator(url: str):
    # bucket_obj = s3.Bucket(event_bucket)
    # url = f"{os.environ['base_url']}{event_uuid}"
    url = pyqrcode.create(url)
    in_mem_file = io.BytesIO()

    url.png(in_mem_file, scale=6)
    qr_bytes = url.png_as_base64_str(scale=8)
    return {"qr_bytes": qr_bytes}
    # in_mem_file.seek(0)
    # print(in_mem_file)
    # bucket_obj.upload_fileobj(in_mem_file, f"{event_name}/metadata/qr.png")
    # return {
    #     "qr_code_location": f"s3://{event_bucket}/{event_name}/metadata/qr.png",
    #     "s3_key": f"{event_name}/metadata/qr.png",
    # }
