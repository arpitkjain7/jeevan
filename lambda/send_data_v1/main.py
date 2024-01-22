from core.controllers.dataTransfer_controller import DataTransferController
from core.utils.aws.s3_helper import read_json
import os
from core.utils.custom.external_call import APIInterface


def handler(event, context):
    try:
        print(event)
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        object_key = event["Records"][0]["s3"]["object"]["key"]
        request_type = object_key.split("/")[-2]
        fhir_json = read_json(bucket_name=bucket_name, prefix=object_key)
        data_push_response = DataTransferController().send_data(
            data_obj=fhir_json, request_type=request_type
        )
        print(f"{data_push_response=}")
    except Exception as error:
        print(f"Error in handler.py : {error}")


# import uvicorn
# from core.apis.api import app
# from mangum import Mangum

# handler = Mangum(app)
# # def handler(event, context):
# # if __name__ == "__main__":
# #     uvicorn.run(app, host="0.0.0.0", port=5000)
