from core.utils.custom.external_call import APIInterface
from datetime import datetime, timezone, timedelta
from core.utils.custom.session_helper import get_session_token
from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from core.utils.fhir.op_consult import opConsultUnstructured
from core.utils.aws.s3_helper import upload_bytes
import os
import uuid
from pytz import timezone as pytz_timezone
from core import logger
import base64, json

logging = logger(__name__)
s3_location = os.environ["s3_location"]


def prepare_data(pmr_id: str):
    try:
        logging.info(f"Preparing data to transfer for {pmr_id=}")
        bundle_id = str(uuid.uuid1())
        return opConsultUnstructured(
            bundle_name=f"OPConsultNote-{bundle_id}",
            bundle_identifier=bundle_id,
            pmr_id=pmr_id,
        )
    except Exception as error:
        logging.error(f"Error in prepare_data function: {error}")
        raise error


def send_data(
    hi_request: dict, consent_obj: dict, transaction_id: str, request_id: str
):
    try:
        logging.info("send_data triggered")
        logging.info(f"{hi_request=}")
        consent_data = consent_obj.get("care_contexts")
        hip_id = consent_obj.get("hip_id")
        care_context_list = consent_data.get("care_context")
        fhir_bundle_list = []
        for care_context_obj in care_context_list:
            logging.info(f"{care_context_obj=}")
            fhir_bundle = prepare_data(
                pmr_id=care_context_obj.get("careContextReference")
            )
            if fhir_bundle:
                fhir_bundle_list.append(
                    {care_context_obj.get("careContextReference"): fhir_bundle}
                )
            else:
                continue
        send_data_obj = {
            "transaction_id": transaction_id,
            "request_id": request_id,
            "hip_id": hip_id,
            "consent_id": consent_obj.get("id"),
            "data_push_url": hi_request.get("dataPushUrl"),
            "receiver_key_material": hi_request.get("keyMaterial"),
            "fhir_bundles": fhir_bundle_list,
        }
        send_data_json = json.dumps(send_data_obj)
        uploaded_file_location = upload_bytes(
            bucket_name=s3_location,
            file_name=f"{hip_id}/{transaction_id}/encrypt/{request_id}.json",
            byte_data=send_data_json,
        )
        return uploaded_file_location
    except Exception as error:
        logging.error(f"Error in send_data function: {error}")
        raise error
