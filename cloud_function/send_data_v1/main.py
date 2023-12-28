from core.controllers.dataTransfer_controller import DataTransferController
from core.utils.aws.s3_helper import read_json
import os
from core.utils.custom.external_call import APIInterface


def handler(event, context):
    try:
        print(event)
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        object_key = event["Records"][0]["s3"]["object"]["key"]
        fhir_json = read_json(bucket_name=bucket_name, prefix=object_key)
        data_push_response = DataTransferController().data_request(data_obj=fhir_json)
        print(f"{data_push_response=}")
    except Exception as error:
        print(f"Error in handler.py : {error}")
