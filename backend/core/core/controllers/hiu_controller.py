from fastapi import HTTPException, status
from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from core.crud.hims_docDetails_crud import CRUDDocDetails
from core.crud.hims_hiu_consent_crud import CRUDHIUConsents
from core.crud.hims_patientDetails_crud import CRUDPatientDetails
from core import logger
from core.utils.custom.external_call import APIInterface
from core.utils.custom.session_helper import get_session_token
import os
import uuid, json
from datetime import datetime, timezone
from core.utils.aws.s3_helper import upload_to_s3
from pytz import timezone as pytz_timezone
from dateutil import parser
import ast

logging = logger(__name__)


class HIUController:
    def __init__(self):
        self.CRUDGatewayInteraction = CRUDGatewayInteraction()
        self.CRUDDocDetails = CRUDDocDetails()
        self.CRUDHIUConsents = CRUDHIUConsents()
        self.CRUDPatientDetails = CRUDPatientDetails()
        self.gateway_url = os.environ["gateway_url"]
        self.s3_location = os.environ["s3_location"]
        self.encryption_base_url = os.environ["encryption_url"]

    def list_consent(self, patient_id: str):
        try:
            return self.CRUDHIUConsents.read_by_patientId(patient_id=patient_id)
        except Exception as error:
            logging.error(f"Error in HIUController.list_consent function: {error}")
            raise error

    def list_approved_consent(self, patient_id: str):
        try:
            patient_obj = self.CRUDPatientDetails.read_by_patientId(
                patient_id=patient_id
            )
            abha_address = patient_obj["abha_address"]
            return self.CRUDHIUConsents.read_approved_by_abhaAddress(
                abha_address=abha_address
            )
        except Exception as error:
            logging.error(f"Error in HIUController.list_consent function: {error}")
            raise error

    def get_consent_details(self, consent_id: str):
        try:
            return self.CRUDHIUConsents.read(consent_id=consent_id)
        except Exception as error:
            logging.error(
                f"Error in HIUController.get_consent_details function: {error}"
            )
            raise error

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
            logging.info(f"{self.gateway_url=}")
            raise_consent_url = f"{self.gateway_url}/v0.5/consent-requests/init"
            logging.info(f"{raise_consent_url=}")
            request_id = str(uuid.uuid1())
            time_now = datetime.now(timezone.utc)
            time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
            logging.info("Calling raise consent url")
            resp_json, resp_code = APIInterface().post(
                route=raise_consent_url,
                data=json.dumps(
                    {
                        "requestId": request_id,
                        "timestamp": time_now,
                        "consent": {
                            "purpose": {
                                "text": purpose.value,
                                "code": purpose.name,
                                "refUri": "www.abdm.gov.in",
                            },
                            "patient": {"id": request_dict["abha_address"]},
                            "hiu": {"id": request_dict["hip_id"]},
                            "consentManager": {"id": "sbx"},
                            # "careContexts": [
                            #     {
                            #         "patientReference": request_dict["abha_address"],
                            #         "careContextReference": "Episode1",
                            #     }
                            # ],
                            # "hip": {"id": request_dict["hip_id"]},
                            # "careContexts": None,
                            "requester": {
                                "name": doc_obj["doc_name"],
                                "identifier": {
                                    "type": "REGNO",
                                    "value": doc_obj["doc_licence_no"],
                                    "system": "https://www.mciindia.org",
                                },
                            },
                            "hiTypes": [
                                "DiagnosticReport",
                                "Prescription",
                                "ImmunizationRecord",
                                "DischargeSummary",
                                "OPConsultation",
                                "HealthDocumentRecord",
                                "WellnessRecord",
                            ],
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
                    }
                ),
                headers={
                    "X-CM-ID": os.environ["X-CM-ID"],
                    "Authorization": f"Bearer {gateway_access_token}",
                    "Content-Type": "application/json",
                },
            )
            logging.debug(f"{resp_code=}")
            if resp_code <= 250:
                crud_request = {
                    "request_id": request_id,
                    "request_type": "CONSENT_INIT",
                    "request_status": "PROCESSING",
                    "callback_response": {
                        "status": "REQUESTED",
                        "patient_id": request_dict["patient_id"],
                        "purpose": purpose.value,
                        "abha_address": request_dict["abha_address"],
                        "hiu_id": request_dict["hip_id"],
                        "hi_type": {"requested_hi_types": hiTypeList},
                        "access_mode": "VIEW",
                        "date_range": {
                            "from": from_date,
                            "to": to_date,
                        },
                        "expire_at": expire_time,
                    },
                }
                self.CRUDGatewayInteraction.create(**crud_request)
                return crud_request
            else:
                crud_request = {
                    "request_id": request_id,
                    "request_type": "CONSENT_INIT",
                    "request_status": "ERROR",
                    "error_code": resp_code,
                    "error_message": resp_json.get("error").get("message"),
                    "callback_response": {
                        "status": "ERROR",
                        "patient_id": request_dict["patient_id"],
                        "purpose": purpose.value,
                        "abha_address": request_dict["abha_address"],
                        "hiu_id": request_dict["hip_id"],
                        "access_mode": "VIEW",
                        "date_range": {
                            "from": from_date,
                            "to": to_date,
                        },
                        "expire_at": expire_time,
                    },
                }
                self.CRUDGatewayInteraction.create(**crud_request)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=crud_request
                )
        except Exception as error:
            logging.error(f"Error in HIUController.raise_consent function: {error}")
            raise error

    def consent_on_init(self, request):
        try:
            logging.info("executing consent_on_init function")
            logging.info(f"{request=}")
            consent_id = request.get("consentRequest").get("id")
            request_id = request.get("resp").get("requestId")
            gateway_obj = self.CRUDGatewayInteraction.read(request_id=request_id)
            consent_request_obj = gateway_obj.get("callback_response")
            consent_request_obj.update({"id": request.get("consentRequest").get("id")})
            self.CRUDHIUConsents.create(**consent_request_obj)
            crud_request = {
                "request_id": request_id,
                "transaction_id": consent_id,
                "request_status": "SUCCESS",
            }
            logging.info("Updating gateway record")
            self.CRUDGatewayInteraction.update(**crud_request)
            return crud_request
        except Exception as error:
            logging.error(f"Error in HIUController.consent_on_init function: {error}")
            raise error

    # def consent_status(self, consent_id: str):
    #     try:
    #         logging.info("executing HIUController.consent_status function")
    #         logging.info(f"{consent_id=}")
    #         gateway_obj = self.CRUDGatewayInteraction.read(request_id=request_id)
    #         consent_request_obj = gateway_obj.get("callback_response")
    #         consent_request_obj.update({"id": request.get("consentRequest").get("id")})
    #         self.CRUDHIUConsents.create(**consent_request_obj)
    #         crud_request = {
    #             "request_id": request_id,
    #             "transaction_id": consent_id,
    #             "request_status": "SUCCESS",
    #         }
    #         logging.info("Updating gateway record")
    #         self.CRUDGatewayInteraction.update(**crud_request)
    #         return crud_request
    #     except Exception as error:
    #         logging.error(f"Error in HIUController.consent_status function: {error}")
    #         raise error

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
                data=json.dumps(
                    {
                        "requestId": request_id,
                        "timestamp": time_now,
                        "query": {
                            "patient": {"id": request_dict["abha_address"]},
                            "requester": {"type": "HIU", "id": request_dict["hiu_id"]},
                        },
                    }
                ),
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
            consent_status = notification_obj.get("status")
            logging.info(f"{consent_status=}")
            if (
                consent_status == "DENIED"
                or consent_status == "REVOKED"
                or consent_status == "EXPIRED"
            ):
                logging.info("Updating consent table record")
                consent_crud_request = {"id": consent_id, "status": consent_status}
                self.CRUDHIUConsents.update(**consent_crud_request)
            else:
                consent_artifact_id = notification_obj.get("consentArtefacts")[0].get(
                    "id"
                )
                logging.info("Updating consent table record")
                consent_crud_request = {
                    "id": consent_id,
                    "status": consent_status,
                    "consent_artifact_id": consent_artifact_id,
                }
                self.CRUDHIUConsents.update(**consent_crud_request)
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
                        data=json.dumps(
                            {
                                "requestId": request_id,
                                "timestamp": time_now,
                                "consentId": consentArtifactId,
                            }
                        ),
                        headers={
                            "X-CM-ID": os.environ["X-CM-ID"],
                            "Authorization": f"Bearer {gateway_access_token}",
                            "Content-Type": "application/json",
                        },
                    )
                    logging.info(
                        f"Response Code for {consentArtifactId=} is {resp_code=}"
                    )
                    # self.CRUDHIUConsents.create(
                    #     **{"id": consentArtifactId, "status": "REQUESTED"}
                    # )
                # if consent_status == "GRANTED":
                #     self.CRUDHIUConsents.create(**consent_crud_request)
                # elif consent_status == "EXPIRED" or consent_status == "REVOKED":
                #     logging.info(f"{consent_crud_request=}")
                #     self.CRUDHIUConsents.update(**consent_crud_request)
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
            hiu_consent_obj = self.CRUDHIUConsents.read_by_consentArtifactId(
                consent_artifact_id=consent_id
            )
            if consent_status == "GRANTED":
                logging.info("Consent granted")
                logging.info(f"{hiu_consent_obj=}")
                logging.info("Updating consent table record")
                valid_date_from = (
                    consent_details.get("permission").get("dateRange").get("from")
                )
                valid_date_to = (
                    consent_details.get("permission").get("dateRange").get("to")
                )
                expire_at = consent_details.get("permission").get("dataEraseAt")
                hi_types = hiu_consent_obj.get("hi_type", {})
                hi_types.update({"granted_hi_types": consent_details.get("hiTypes")})
                self.CRUDHIUConsents.update(
                    **{
                        "id": hiu_consent_obj.get("id"),
                        "status": consent_status,
                        "purpose": consent_details.get("purpose").get("text"),
                        "abha_address": consent_details.get("patient").get("id"),
                        "hip_id": consent_details.get("hip").get("id"),
                        "hip_name": consent_details.get("hip").get("name"),
                        "hiu_id": consent_details.get("hiu").get("id"),
                        "hiu_name": consent_details.get("requester").get("name"),
                        "hi_type": hi_types,
                        "access_mode": consent_details.get("permission").get(
                            "accessMode"
                        ),
                        "date_range": {
                            "from": valid_date_from,
                            "to": valid_date_to,
                        },
                        "expire_at": expire_at,
                        "care_contexts": {
                            "care_context": consent_details.get("careContexts")
                        },
                    }
                )
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
                requester_key_material, response_code = APIInterface().get(
                    route=f"{self.encryption_base_url}/v1/cliniq360/generateKey"
                )
                logging.info(f"{requester_key_material=}")
                self.CRUDHIUConsents.update(
                    **{
                        "id": hiu_consent_obj.get("id"),
                        "requester_key_material": requester_key_material,
                    }
                )
                _, resp_code = APIInterface().post(
                    route=health_info_url,
                    data=json.dumps(
                        {
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
                                        "keyValue": requester_key_material.get(
                                            "publicKey"
                                        ),
                                    },
                                    "nonce": requester_key_material.get("nonce"),
                                },
                            },
                        }
                    ),
                    headers={
                        "X-CM-ID": os.environ["X-CM-ID"],
                        "Authorization": f"Bearer {gateway_access_token}",
                        "Content-Type": "application/json",
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
                consent_crud_request = {
                    "id": hiu_consent_obj.get("id"),
                    "status": consent_status,
                    "patient_data_raw": None,
                    "patient_data_transformed": None,
                }
                self.CRUDHIUConsents.update(**consent_crud_request)
            elif consent_status == "DENIED":
                logging.info("Consent denied")
                logging.info("Creating consent table record")
                consent_crud_request = {
                    "id": hiu_consent_obj.get("id"),
                    "status": consent_status,
                }
                self.CRUDHIUConsents.update(**consent_crud_request)
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
            # gateway_obj = self.CRUDGatewayInteraction.read_by_transId(
            #     transaction_id=transaction_id, request_type="DATA_TRANSFER_TRIGGERED"
            # )
            gateway_obj = self.CRUDGatewayInteraction.read_by_transId_v1(
                transaction_id=transaction_id
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
            consent_id = consent_details.get("consent").get("id")
            logging.info(f"{consent_id=}")
            consent_obj = self.CRUDHIUConsents.read_by_consentArtifactId(
                consent_artifact_id=consent_id
            )
            requester_key_material = consent_obj.get("requester_key_material")
            logging.info(f"{requester_key_material=}")
            patient_data_list = []
            resources_dict = {}
            patient_data_transformed = []
            decrypt_payload = request.copy()
            decrypt_payload.update(
                {
                    "requesterNonce": requester_key_material.get("nonce"),
                    "senderNonce": sender_key_material.get("nonce"),
                    "requesterPrivateKey": requester_key_material.get("privateKey"),
                    "senderPublicKey": sender_key_material.get("dhPublicKey").get(
                        "keyValue"
                    ),
                }
            )
            # consent_obj = self.CRUDHIUConsents.read(consent_id=consent_id)
            hip_id = consent_obj.get("hip_id")
            send_data_json = json.dumps(decrypt_payload)
            uploaded_file_location = upload_to_s3(
                bucket_name=self.s3_location,
                file_name=f"{hip_id}/{transaction_id}/encrypt/{gateway_obj['request_id']}.json",
                byte_data=send_data_json,
            )
            return uploaded_file_location
        except Exception as error:
            logging.error(
                f"Error in HIUController.hiu_process_patient_data function: {error}"
            )
            raise error

    def hiu_store_patient_data(self, request):
        try:
            logging.info(f"{request=}")
            self.CRUDHIUConsents.update(
                **{
                    "id": request.get("consent_id"),
                    "patient_data_raw": request.get("patient_data_list"),
                    "patient_data_transformed": request.get("patient_data_transformed"),
                }
            )
            return {"satatus": "success"}
        except Exception as error:
            logging.error(
                f"Error in HIUController.hiu_store_patient_data function: {error}"
            )
            raise error
