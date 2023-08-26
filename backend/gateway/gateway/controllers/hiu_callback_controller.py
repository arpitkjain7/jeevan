from gateway.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from gateway.crud.hims_hiu_consent_crud import CRUDHIUConsents
from gateway import logger
from gateway.utils.custom.external_call import APIInterface
from gateway.utils.custom.session_helper import get_session_token
from gateway.utils.custom.encryption_helper import getEcdhKeyMaterial, decryptData
import os
import uuid, json
from datetime import datetime, timezone
from pytz import timezone as pytz_timezone
from gateway import celery

logging = logger(__name__)


class HIUCallbackController:
    def __init__(self):
        self.CRUDGatewayInteraction = CRUDGatewayInteraction()
        self.CRUDHIUConsents = CRUDHIUConsents()
        self.gateway_url = os.environ["gateway_url"]

    def consent_on_init(self, request):
        try:
            logging.info("executing consent_on_init function")
            logging.info(f"{request=}")
            consent_id = request.get("consentRequest").get("id")
            request_id = request.get("resp").get("requestId")
            crud_request = {
                "request_id": request_id,
                "transaction_id": consent_id,
                "request_status": "SUCCESS",
            }
            logging.info("Creating gateway record")
            self.CRUDGatewayInteraction.update(**crud_request)
            return crud_request
        except Exception as error:
            logging.error(f"Error in HIUController.consent_on_init function: {error}")
            raise error

    def on_find_patient(self, request):
        try:
            logging.info("executing on_find_patient function")
            logging.info(f"{request=}")
            logging.info("Getting session access Token")
            patient_data = request["patient"]
            request_id = request["resp"]["requestId"]
            if patient_data:
                crud_request = {
                    "request_id": request_id,
                    "request_status": "SUCCESS",
                    "callback_response": request,
                }
            else:
                crud_request = {
                    "request_id": request_id,
                    "request_status": "FAILED",
                    "callback_response": request,
                }
            self.CRUDGatewayInteraction.update(**crud_request)
            return crud_request
        except Exception as error:
            logging.error(f"Error in HIUController.on_find_patient function: {error}")
            raise error

    def hiu_notify(self, request):
        try:
            logging.info("executing hiu_notify function")
            logging.info(f"{request=}")
            notification_obj = request.get("notification")
            consent_id = notification_obj.get("consentRequestId")
            logging.info("Updating consent table record")
            consent_crud_request = {
                "id": consent_id,
                "status": notification_obj.get("status"),
            }
            logging.info("Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            fetch_consent_url = f"{self.gateway_url}/v0.5/consents/fetch"
            for consentArtifact in notification_obj.get("consentArtefacts"):
                consentArtifactId = consentArtifact.get("id")
                request_id = str(uuid.uuid1())
                time_now = datetime.now(timezone.utc)
                time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
                _, resp_code = APIInterface().post(
                    route=fetch_consent_url,
                    data={
                        "requestId": request_id,
                        "timestamp": time_now,
                        "consentId": consentArtifactId,
                    },
                    headers={
                        "X-CM-ID": os.environ["X-CM-ID"],
                        "Authorization": f"Bearer {gateway_access_token}",
                    },
                )
                logging.info(f"Response Code for {consentArtifactId=} is {resp_code=}")
                # self.CRUDHIUConsents.create(
                #     **{"id": consentArtifactId, "status": "REQUESTED"}
                # )
            self.CRUDHIUConsents.create(**consent_crud_request)
        except Exception as error:
            logging.error(f"Error in HIUController.hiu_notify function: {error}")
            raise error

    def hiu_fetch_consent(self, request):
        try:
            logging.info("executing  hiu_fetch_consent function")
            consent_obj = request.get("consent")
            consent_status = consent_obj.get("status")
            consent_details = consent_obj.get("consentDetail")
            consent_id = consent_details.get("consentId")
            request_id = request.get("requestId")
            if consent_status == "GRANTED":
                logging.info("Consent granted")
                logging.info("Creating consent table record")
                valid_date_from = (
                    consent_details.get("permission").get("dateRange").get("from")
                )
                valid_date_to = (
                    consent_details.get("permission").get("dateRange").get("to")
                )
                expire_at = consent_details.get("permission").get("dataEraseAt")
                consent_crud_request = {
                    "id": consent_id,
                    "status": consent_status,
                    "purpose": consent_details.get("purpose").get("text"),
                    "patient": consent_details.get("patient").get("id"),
                    "hip_id": consent_details.get("hip").get("id"),
                    "hip_name": consent_details.get("hip").get("name"),
                    "hiu_id": consent_details.get("hiu").get("id"),
                    "hiu_name": consent_details.get("requester").get("name"),
                    "hi_type": {"hi_types": consent_details.get("hiTypes")},
                    "access_mode": consent_details.get("permission").get("accessMode"),
                    "date_range": {
                        "from": valid_date_from,
                        "to": valid_date_to,
                    },
                    "expire_at": expire_at,
                    "care_contexts": {
                        "care_context": consent_details.get("careContexts")
                    },
                }
                self.CRUDHIUConsents.create(**consent_crud_request)
                logging.info("Sending health information request")
                logging.info("Getting session access Token")
                gateway_access_token = get_session_token(
                    session_parameter="gateway_token"
                ).get("accessToken")
                health_info_url = (
                    f"{self.gateway_url}/v0.5/health-information/cm/request"
                )
                request_id = str(uuid.uuid1())
                time_now = datetime.now(timezone.utc)
                time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
                requester_key_material = getEcdhKeyMaterial()
                self.CRUDHIUConsents.update(
                    **{
                        "id": consent_id,
                        "requester_key_material": requester_key_material,
                    }
                )
                _, resp_code = APIInterface().post(
                    route=health_info_url,
                    data={
                        "requestId": request_id,
                        "timestamp": time_now,
                        "hiRequest": {
                            "consent": {"id": consent_id},
                            "dateRange": {
                                "from": valid_date_from,
                                "to": valid_date_to,
                            },
                            "dataPushUrl": os.environ["data_push_url"],
                            "keyMaterial": {
                                "cryptoAlg": "ECDH",
                                "curve": "Curve25519",
                                "dhPublicKey": {
                                    "expiry": expire_at,
                                    "parameters": "Curve25519/32byte random key",
                                    "keyValue": requester_key_material.get("publicKey"),
                                },
                                "nonce": requester_key_material.get("nonce"),
                            },
                        },
                    },
                    headers={
                        "X-CM-ID": os.environ["X-CM-ID"],
                        "Authorization": f"Bearer {gateway_access_token}",
                    },
                )
                logging.info(f"Response Code is {resp_code=}")
                crud_request = {
                    "request_id": request_id,
                    "request_status": "PROCESSING",
                    "request_type": "DATA_TRANSFER_TRIGGERED",
                    "callback_response": {
                        "consent_id": consent_id,
                        "requester_key_material": requester_key_material,
                    },
                }
                self.CRUDGatewayInteraction.create(**crud_request)
            elif consent_status == "EXPIRED" or consent_status == "REVOKED":
                logging.info("Consent expired or revoked")
                logging.info("Creating consent table record")
                consent_crud_request = {"id": consent_id, "status": consent_status}
                self.CRUDHIUConsents.create(**consent_crud_request)
            elif consent_status == "DENIED":
                logging.info("Consent denied")
                logging.info("Creating consent table record")
                consent_crud_request = {"id": consent_id, "status": consent_status}
                self.CRUDHIUConsents.create(**consent_crud_request)
        except Exception as error:
            logging.error(f"Error in HIUController.hiu_fetch_consent function: {error}")
            raise error

    def health_info_hiu_on_request(self, request):
        try:
            logging.info("executing health_info_hiu_on_request function")
            logging.info(f"{request=}")
            transaction_id = request["hiRequest"]["transactionId"]
            request_id = request["resp"]["requestId"]
            crud_request = {
                "request_id": request_id,
                "request_status": "ACK",
                "transaction_id": transaction_id,
            }
            self.CRUDGatewayInteraction.update(**crud_request)
        except Exception as error:
            logging.error(
                f"Error in HIUController.health_info_hiu_on_request function: {error}"
            )
            raise error

    def hiu_process_patient_data(self, request):
        try:
            logging.info("executing hiu_process_patient_data function")
            logging.info(f"{request=}")
            transaction_id = request["transactionId"]
            gateway_obj = self.CRUDGatewayInteraction.read_by_transId(
                transaction_id=transaction_id, request_type="DATA_TRANSFER_TRIGGERED"
            )
            logging.info(f"{gateway_obj=}")
            crud_request = {
                "request_id": gateway_obj["request_id"],
                "callback_response": request,
                "request_status": "DECRYPTING",
            }
            self.CRUDGatewayInteraction.update(**crud_request)
            patient_data = request["entries"]
            sender_key_material = request["keyMaterial"]
            consent_details = gateway_obj.get("callback_response")
            logging.info(f"{consent_details=}")
            consent_id = consent_details.get("consent_id")
            logging.info(f"{consent_id=}")
            requester_key_material = consent_details.get("requester_key_material")
            logging.info(f"{requester_key_material=}")
            patient_data_list = []
            for entry in patient_data:
                encrypted_data = entry.get("content")
                decrypted_data = decryptData(
                    decryptParams={
                        "encryptedData": encrypted_data,
                        "requesterNonce": requester_key_material.get("nonce"),
                        "senderNonce": sender_key_material.get("nonce"),
                        "requesterPrivateKey": requester_key_material.get("privateKey"),
                        "senderPublicKey": sender_key_material.get("dhPublicKey").get(
                            "keyValue"
                        ),
                    }
                )
                logging.info(f"{decrypted_data=}")
                logging.info(type(decrypted_data))
                decrypted_json = json.loads(decrypted_data)
                logging.info(f"{decrypted_json=}")
                logging.info(type(decrypted_json))
                fhir_data = decrypted_json.get("decryptedData")
                logging.info(f"{fhir_data=}")
                logging.info(type(fhir_data))
                fhir_string = fhir_data.replace("'", '"')
                fhir_json = json.loads(fhir_string)
                logging.info(f"{fhir_json=}")
                logging.info(type(fhir_json))
                patient_data_list.append(fhir_json)
            logging.info(f"{patient_data_list=}")
            self.CRUDHIUConsents.update(
                **{"id": consent_id, "patient_data_raw": patient_data_list}
            )
            return {"satatus": "success"}
        except Exception as error:
            logging.error(
                f"Error in HIUController.hiu_process_patient_data function: {error}"
            )
            raise error
