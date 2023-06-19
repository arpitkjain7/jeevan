from core.crud.hims_hip_crud import CRUDHIP
from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from core.crud.hims_docDetails_crud import CRUDDocDetails
from core.crud.hims_hiu_consent_crud import CRUDHIUConsents
from core import logger
from core.utils.custom.external_call import APIInterface
from core.utils.custom.session_helper import get_session_token
from core.utils.custom.encryption_helper import getEcdhKeyMaterial
import os
import uuid
from datetime import datetime, timezone
from pytz import timezone as pytz_timezone
from dateutil import parser
from core import celery

logging = logger(__name__)


class HIUController:
    def __init__(self):
        self.CRUDHIP = CRUDHIP()
        self.CRUDGatewayInteraction = CRUDGatewayInteraction()
        self.CRUDDocDetails = CRUDDocDetails()
        self.CRUDHIUConsents = CRUDHIUConsents()
        self.gateway_url = os.environ["gateway_url"]

    def raise_consent(self, request):
        """[Controller to create new hip record]

        Args:
            request ([dict]): [create new hip request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing raise_consent function")
            request_dict = request.dict()
            logging.info(f"{request_dict=}")
            hiTypeList = []
            for hi_type in request_dict.get("hi_type"):
                hiTypeList.append(hi_type.name)
            expire_datetime_object = parser.parse(request_dict.get("expiry"))
            logging.info(f"{expire_datetime_object=}")
            expire_time = expire_datetime_object.strftime("%Y-%m-%dT%H:%M:%S.%f")
            logging.info(f"{expire_time=}")
            from_datetime_object = parser.parse(request_dict.get("date_from"))
            logging.info(f"{from_datetime_object=}")
            from_date = from_datetime_object.strftime("%Y-%m-%dT%H:%M:%S.%f")
            logging.info(f"{from_date=}")
            to_datetime_object = parser.parse(request_dict.get("date_to"))
            logging.info(f"{to_datetime_object=}")
            to_date = to_datetime_object.strftime("%Y-%m-%dT%H:%M:%S.%f")
            logging.info(f"{to_date=}")
            purpose = request_dict.get("purpose")
            doc_obj = self.CRUDDocDetails.read_by_docId(doc_id=request_dict["doc_id"])
            logging.info("Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            raise_consent_url = f"{self.gateway_url}/v0.5/consent-requests/init"
            request_id = str(uuid.uuid1())
            time_now = datetime.now(timezone.utc)
            time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
            _, resp_code = APIInterface().post(
                route=raise_consent_url,
                data={
                    "requestId": request_id,
                    "timestamp": time_now,
                    "consent": {
                        "purpose": {
                            "text": purpose.value,
                            "code": purpose.name,
                        },
                        "patient": {"id": request_dict["abha_address"]},
                        "hiu": {"id": request_dict["hip_id"]},
                        "requester": {
                            "name": doc_obj["doc_name"],
                            "identifier": {
                                "type": "REGNO",
                                "value": doc_obj["doc_reg_id"],
                                "system": "https://www.mciindia.org",
                            },
                        },
                        "hiTypes": hiTypeList,
                        "permission": {
                            "accessMode": "VIEW",
                            "dateRange": {
                                "from": from_date,
                                "to": to_date,
                            },
                            "dataEraseAt": expire_time,
                            "frequency": {"unit": "HOUR", "value": 1, "repeats": 0},
                        },
                    },
                },
                headers={
                    "X-CM-ID": os.environ["X-CM-ID"],
                    "Authorization": f"Bearer {gateway_access_token}",
                },
            )
            logging.debug(f"{resp_code=}")
            crud_request = {
                "request_id": request_id,
                "request_type": "CONSENT_INIT",
                "request_status": "PROCESSING",
            }
            self.CRUDGatewayInteraction.create(**crud_request)
            return crud_request
        except Exception as error:
            logging.error(f"Error in HIUController.raise_consent function: {error}")
            raise error

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
            logging.info("Creating consent table record")
            consent_crud_request = {"id": consent_id, "status": "REQUESTED"}
            self.CRUDHIUConsents.create(**consent_crud_request)
            return crud_request
        except Exception as error:
            logging.error(f"Error in HIUController.consent_on_init function: {error}")
            raise error

    def find_patient(self, request):
        try:
            logging.info("executing find_patient function")
            request_dict = request.dict()
            logging.info(f"{request_dict=}")
            logging.info("Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            find_patient_url = f"{self.gateway_url}/v0.5/patients/find"
            request_id = str(uuid.uuid1())
            time_now = datetime.now(timezone.utc)
            time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
            _, resp_code = APIInterface().post(
                route=find_patient_url,
                data={
                    "requestId": request_id,
                    "timestamp": time_now,
                    "query": {
                        "patient": {"id": request_dict["abha_address"]},
                        "requester": {"type": "HIU", "id": request_dict["hiu_id"]},
                    },
                },
                headers={
                    "X-CM-ID": os.environ["X-CM-ID"],
                    "Authorization": f"Bearer {gateway_access_token}",
                },
            )
            logging.debug(f"{resp_code=}")
            crud_request = {
                "request_id": request_id,
                "request_type": "FIND_PATIENT",
                "request_status": "PROCESSING",
            }
            self.CRUDGatewayInteraction.create(**crud_request)
            return crud_request
        except Exception as error:
            logging.error(f"Error in HIUController.find_patient function: {error}")
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
                sender_key_material = getEcdhKeyMaterial()
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
                                    "keyValue": sender_key_material.get("publicKey"),
                                },
                                "nonce": sender_key_material.get("nonce"),
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
            request_id = request["resp"]["requestId"]
            transaction_id = request["hiRequest"]["transactionId"]
            transaction_status = request["hiRequest"]["sessionStatus"]
            crud_request = {
                "request_id": request_id,
                "request_status": transaction_status,
                "transaction_id": transaction_id,
                "callback_response": request,
            }
            self.CRUDGatewayInteraction.update(**crud_request)
            return crud_request
        except Exception as error:
            logging.error(
                f"Error in HIUController.health_info_hiu_on_request function: {error}"
            )
            raise error