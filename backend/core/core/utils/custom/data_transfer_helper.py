from core.utils.custom.encryption_helper import (
    encrypt_data,
    getEcdhKeyMaterial,
    generateChecksum,
)
from core.utils.custom.external_call import APIInterface
from datetime import datetime, timezone, timedelta
from core.utils.custom.session_helper import get_session_token
from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from core.utils.fhir.op_consult import opConsultUnstructured
from core.utils.aws.s3_helper import upload_to_s3
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
        # data_push_url = hi_request.get("dataPushUrl")
        # key_material = hi_request.get("keyMaterial")
        consent_data = consent_obj.get("care_contexts")
        hip_id = consent_obj.get("hip_id")
        care_context_list = consent_data.get("care_context")
        care_context_output, care_context_ack = [], []
        fhir_bundle_list = []
        # sender_key_material = getEcdhKeyMaterial()  # lambda
        for care_context_obj in care_context_list:
            logging.info(f"{care_context_obj=}")
            fhir_bundle = prepare_data(
                pmr_id=care_context_obj.get("careContextReference")
            )
            if fhir_bundle:
                fhir_bundle_list.append(
                    {care_context_obj.get("careContextReference"): fhir_bundle}
                )
                # checksum = generateChecksum(json_data=fhir_bundle)
                # encryption_obj = encrypt_data(
                #     stringToEncrypt=f"{fhir_bundle}",
                #     requesterKeyMaterial=key_material,
                #     senderKeyMaterial=sender_key_material,
                # )
                # encrypted_data = encryption_obj.get("encryptedData")
                # care_context_output.append(
                #     {
                #         "content": encrypted_data,
                #         "media": "application/fhir+json",
                #         "checksum": checksum,
                #         "careContextReference": care_context_obj.get(
                #             "careContextReference"
                #         ),
                #     }
                # )
                # care_context_ack.append(
                #     {
                #         "careContextReference": care_context_obj.get(
                #             "careContextReference"
                #         ),
                #         "hiStatus": "OK",
                #         "description": "Transfered Successfully",
                #     }
                # )
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
        uploaded_file_location = upload_to_s3(
            bucket_name=s3_location,
            file_name=f"{hip_id}/{transaction_id}/{request_id}.json",
            byte_data=send_data_json,
        )
        # data_request = {
        #     "pageNumber": 0,
        #     "pageCount": 1,
        #     "transactionId": transaction_id,
        #     "entries": care_context_output,
        #     "keyMaterial": {
        #         "cryptoAlg": "ECDH",
        #         "curve": "Curve25519",
        #         "dhPublicKey": {
        #             "expiry": "2024-10-06T10:50:37.764Z",
        #             "parameters": "Curve25519/32byte random key",
        #             "keyValue": sender_key_material.get("x509PublicKey"),
        #         },
        #         "nonce": sender_key_material.get("nonce"),
        #     },
        # }
        # with open(
        #     f"/app/core/utils/custom/output-{str(uuid.uuid1().int)[:18]}.json", "w"
        # ) as json_file:
        #     json.dump(data_request, json_file)
        # _, resp_code = APIInterface().post(route=data_push_url, data=data_request)
        # logging.info(f"Data push {resp_code=}")
        return uploaded_file_location
    except Exception as error:
        logging.error(f"Error in send_data function: {error}")
        raise error
