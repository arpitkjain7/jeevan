from gateway.utils.custom.encryption_helper import (
    encrypt_data,
    getEcdhKeyMaterial,
    generateChecksum,
)
from gateway.utils.custom.external_call import APIInterface
from datetime import datetime, timezone, timedelta
from gateway.utils.custom.session_helper import get_session_token
from gateway.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from gateway.utils.fhir.op_consult import opConsultDocument
import os
import uuid
from pytz import timezone as pytz_timezone
from gateway import logger
from gateway import celery
import base64

logging = logger(__name__)


def prepare_data(pmr_id: str):
    try:
        logging.info(f"Preparing data to transfer for {pmr_id=}")
        bundle_id = str(uuid.uuid1())
        op_consult_document = opConsultDocument(
            bundle_name=f"OPConsultNote-{bundle_id}",
            bundle_identifier=bundle_id,
            pmr_id=pmr_id,
        )
        logging.debug(f"{op_consult_document=}")
        return op_consult_document
    except Exception as error:
        logging.error(f"Error in prepare_data function: {error}")
        raise error


def send_data(
    hi_request: dict, consent_obj: dict, transaction_id: str, request_id: str
):
    try:
        logging.info("send_data triggered")
        logging.info(f"{hi_request=}")
        data_push_url = hi_request.get("dataPushUrl")
        key_material = hi_request.get("keyMaterial")
        consent_data = consent_obj.get("care_contexts")
        hip_id = consent_obj.get("hip_id")
        care_context_list = consent_data.get("care_context")
        care_context_output, care_context_ack = [], []
        sender_key_material = getEcdhKeyMaterial()
        for care_context_obj in care_context_list:
            logging.info(f"{care_context_obj=}")
            # with open("/app/core/utils/custom/arpit-abha-card.pdf", "rb") as pdf_file:
            #     pdf_data = pdf_file.read()
            #     base64_data = base64.b64encode(pdf_data)
            #     encoded_string = base64_data.decode("utf-8")
            fhir_bundle = prepare_data(
                pmr_id=care_context_obj.get("careContextReference")
            )
            if fhir_bundle:
                checksum = generateChecksum(json_data=fhir_bundle)
                encryption_obj = encrypt_data(
                    stringToEncrypt=f"{fhir_bundle}",
                    requesterKeyMaterial=key_material,
                    senderKeyMaterial=sender_key_material,
                )
                encrypted_data = encryption_obj.get("encryptedData")
                care_context_output.append(
                    {
                        "content": encrypted_data,
                        "media": "application/fhir+json",
                        "checksum": checksum,
                        "careContextReference": care_context_obj.get(
                            "careContextReference"
                        ),
                    }
                )
                care_context_ack.append(
                    {
                        "careContextReference": care_context_obj.get(
                            "careContextReference"
                        ),
                        "hiStatus": "OK",
                        "description": "Transfered Successfully",
                    }
                )
            else:
                continue
        # logging.info(f"{care_context_output=}")
        data_request = {
            "pageNumber": 0,
            "pageCount": 1,
            "transactionId": transaction_id,
            "entries": care_context_output,
            "keyMaterial": {
                "cryptoAlg": "ECDH",
                "curve": "Curve25519",
                "dhPublicKey": {
                    "expiry": "2024-10-06T10:50:37.764Z",
                    "parameters": "Curve25519/32byte random key",
                    "keyValue": sender_key_material.get("x509PublicKey"),
                },
                "nonce": sender_key_material.get("nonce"),
            },
        }
        _, resp_code = APIInterface().post(route=data_push_url, data=data_request)
        logging.info(f"Data push {resp_code=}")
        ack_request_id = str(uuid.uuid1())
        time_now = datetime.now(timezone.utc)
        time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
        gateway_access_token = get_session_token(session_parameter="gateway_token").get(
            "accessToken"
        )
        gateway_url = os.environ["gateway_url"]
        data_transfer_success_url = f"{gateway_url}/v0.5/health-information/notify"
        request = {
            "requestId": ack_request_id,
            "timestamp": time_now,
            "notification": {
                "consentId": consent_obj.get("id"),
                "transactionId": transaction_id,
                "doneAt": time_now,
                "notifier": {"type": "HIP", "id": hip_id},
                "statusNotification": {
                    "sessionStatus": "TRANSFERRED",
                    "hipId": hip_id,
                    "statusResponses": care_context_ack,
                },
            },
        }
        headers = {
            "X-CM-ID": os.environ["X-CM-ID"],
            "Authorization": f"Bearer {gateway_access_token}",
        }
        _, ack_resp_code = APIInterface().post(
            route=data_transfer_success_url, data=request, headers=headers
        )
        logging.info(f"ack sent {ack_resp_code=}")
        gateway_request = {"request_id": request_id}
        if ack_resp_code <= 250:
            gateway_request.update({"request_status": "SUCCESS"})
        else:
            gateway_request.update({"request_status": "FAILED"})
        CRUDGatewayInteraction().update(**gateway_request)
        return gateway_request
    except Exception as error:
        logging.error(f"Error in send_data function: {error}")
        raise error
