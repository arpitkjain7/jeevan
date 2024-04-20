from core.crud.hims_patientDetails_crud import CRUDPatientDetails
from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from core.crud.hims_hip_crud import CRUDHIP
from core.crud.hims_patientMedicalRecord_crud import CRUDPatientMedicalRecord
from core.crud.hims_consent_crud import CRUDConsents
from core.utils.custom.data_transfer_helper import send_data
from core.utils.custom.external_call import APIInterface
from core.utils.custom.session_helper import get_session_token
from core import logger
from datetime import datetime, timezone, timedelta
import os, json
import uuid
from pytz import timezone as pytz_timezone
from dateutil import parser

logging = logger(__name__)


class DataTransferController:
    def __init__(self):
        self.CRUDPatientDetails = CRUDPatientDetails()
        self.CRUDGatewayInteraction = CRUDGatewayInteraction()
        self.CRUDHIP = CRUDHIP()
        self.CRUDPatientMedicalRecord = CRUDPatientMedicalRecord()
        self.CRUDConsents = CRUDConsents()
        self.gateway_url = os.environ["gateway_url"]

    def hip_notify(self, request):
        try:
            request_id = request.get("requestId")
            logging.info(f"Request ID : {request_id} : executing  hip_notify function")
            logging.info(f"Request ID : {request_id} : Creating gateway record")
            notification_obj = request.get("notification")
            consent_status = notification_obj.get("status")
            consent_id = notification_obj.get("consentId")
            consent_details = notification_obj.get("consentDetail")
            if consent_status == "GRANTED":
                logging.info(f"Request ID : {request_id} : Consent granted")
                crud_request = {
                    "request_id": request_id,
                    "request_type": "CONSENT_NOTIFY_GRANT",
                    "request_status": "PROCESSING",
                    "transaction_id": consent_id,
                    "callback_response": consent_details,
                }
                self.CRUDGatewayInteraction.create(**crud_request)
                logging.info(
                    f"Request ID : {request_id} : Creating consent table record"
                )
                consent_crud_request = {
                    "id": consent_id,
                    "status": consent_status,
                    "purpose": consent_details.get("purpose").get("text"),
                    "patient": consent_details.get("patient").get("id"),
                    "hip_id": consent_details.get("hip").get("id"),
                    "hip_name": consent_details.get("hip").get("name"),
                    "hi_type": {"hi_types": consent_details.get("hiTypes")},
                    "access_mode": consent_details.get("permission").get("accessMode"),
                    "date_range": {
                        "from": consent_details.get("permission")
                        .get("dateRange")
                        .get("from"),
                        "to": consent_details.get("permission")
                        .get("dateRange")
                        .get("to"),
                    },
                    "expire_at": consent_details.get("permission").get("dataEraseAt"),
                    "care_contexts": {
                        "care_context": consent_details.get("careContexts")
                    },
                }
                self.CRUDConsents.create(**consent_crud_request)
            elif consent_status == "EXPIRED" or consent_status == "REVOKED":
                logging.info(f"Request ID : {request_id} : Consent expired or revoked")
                crud_request = {
                    "request_id": request_id,
                    "request_type": "CONSENT_NOTIFY_EXPIRE",
                    "request_status": "PROCESSING",
                    "transaction_id": consent_id,
                    "callback_response": consent_details,
                }
                self.CRUDGatewayInteraction.create(**crud_request)
                logging.info(
                    f"Request ID : {request_id} : Creating consent table record"
                )
                consent_crud_request = {"id": consent_id, "status": consent_status}
                self.CRUDConsents.update(**consent_crud_request)
            elif consent_status == "DENIED":
                logging.info(f"Request ID : {request_id} : Consent denied")
                crud_request = {
                    "request_id": request_id,
                    "request_type": "CONSENT_NOTIFY_DENIED",
                    "request_status": "PROCESSING",
                    "transaction_id": consent_id,
                    "callback_response": consent_details,
                }
                self.CRUDGatewayInteraction.create(**crud_request)
                logging.info(
                    f"Request ID : {request_id} : Creating consent table record"
                )
                consent_crud_request = {"id": consent_id, "status": consent_status}
                self.CRUDConsents.update(**consent_crud_request)
            logging.info(f"Request ID : {request_id} : Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            consent_on_notify_url = f"{self.gateway_url}/v0.5/consents/hip/on-notify"
            notify_request_id = str(uuid.uuid1())
            time_now = datetime.now(timezone.utc)
            time_now = time_now + timedelta(seconds=300)
            time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S")
            _, resp_code = APIInterface().post(
                route=consent_on_notify_url,
                data=json.dumps(
                    {
                        "requestId": notify_request_id,
                        "timestamp": time_now,
                        "acknowledgement": {
                            "status": "OK",
                            "consentId": consent_id,
                        },
                        "resp": {"requestId": request_id},
                    }
                ),
                headers={
                    "X-CM-ID": os.environ["X-CM-ID"],
                    "Authorization": f"Bearer {gateway_access_token}",
                    "Content-Type": "application/json",
                },
            )
            logging.debug(f"Request ID : {request_id} : {resp_code=}")
            gateway_request = {"request_id": request_id}
            if resp_code <= 250:
                gateway_request.update({"request_status": "SUCCESS"})
            else:
                gateway_request.update({"request_status": "FAILED"})
            self.CRUDGatewayInteraction.update(**gateway_request)
            return gateway_request
        except Exception as error:
            logging.error(
                f"Request ID : {request_id} : Error in DataTransferController.hip_notify function: {error}"
            )
            raise error

    def data_request(self, request):
        try:
            logging.info("executing  data_request function")
            logging.info("Creating gateway record")
            transaction_id = request.get("transactionId")
            request_id = request.get("requestId")
            hi_request_obj = request.get("hiRequest")
            consent_id = hi_request_obj.get("consent").get("id")
            consent_obj = CRUDConsents().read(consent_id=consent_id)
            gateway_url = os.environ["gateway_url"]
            consent_on_notify_url = (
                f"{gateway_url}/v0.5/health-information/hip/on-request"
            )
            time_now = datetime.now(timezone.utc)
            logging.info(f"{time_now=}")
            expire_datetime_object = parser.parse(consent_obj.get("expire_at"))
            logging.info(f"{expire_datetime_object=}")
            utc_timezone = pytz_timezone("UTC")
            logging.info(f"{utc_timezone=}")
            # expire_time_utc = utc_timezone.localize(expire_datetime_object)
            # logging.info(f"{expire_time_utc=}")
            expire_time = expire_datetime_object.strftime("%Y-%m-%dT%H:%M:%S")
            logging.info(f"{expire_time=}")
            if (
                time_now < expire_datetime_object
                and consent_obj.get("status") == "GRANTED"
            ):
                crud_request = {
                    "request_id": request_id,
                    "request_type": "DATA_REQUEST",
                    "request_status": "PROCESSING",
                    "transaction_id": transaction_id,
                    "callback_response": hi_request_obj,
                }
                CRUDGatewayInteraction().update(**crud_request)
                logging.info("Getting session access Token")
                gateway_access_token = get_session_token(
                    session_parameter="gateway_token"
                ).get("accessToken")
                notify_request_id = str(uuid.uuid1())
                time_now = datetime.now(timezone.utc)
                time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S")
                _, resp_code = APIInterface().post(
                    route=consent_on_notify_url,
                    data=json.dumps(
                        {
                            "requestId": notify_request_id,
                            "timestamp": time_now,
                            "hiRequest": {
                                "transactionId": transaction_id,
                                "sessionStatus": "ACKNOWLEDGED",
                            },
                            "resp": {"requestId": request_id},
                        }
                    ),
                    headers={
                        "X-CM-ID": os.environ["X-CM-ID"],
                        "Authorization": f"Bearer {gateway_access_token}",
                        "Content-Type": "application/json",
                    },
                )
                logging.debug("Request acknowledged")
                logging.debug(f"{resp_code=}")
                hi_request = request.get("hiRequest")
                logging.debug("preparing data as background task")
                logging.info(
                    f"{hi_request=},{consent_id=},{transaction_id=},{request_id=}"
                )
                uploaded_file_location = send_data(
                    hi_request=request.get("hiRequest"),
                    consent_obj=consent_obj,
                    transaction_id=transaction_id,
                    request_id=request_id,
                )
                return {
                    "status": "success",
                    "details": f"File loaded to S3 : {uploaded_file_location}",
                }
            else:
                logging.info("Getting session access Token")
                gateway_access_token = get_session_token(
                    session_parameter="gateway_token"
                ).get("accessToken")
                notify_request_id = str(uuid.uuid1())
                time_now = datetime.now(timezone.utc)
                time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S")
                _, resp_code = APIInterface().post(
                    route=consent_on_notify_url,
                    data=json.dumps(
                        {
                            "requestId": notify_request_id,
                            "timestamp": time_now,
                            "hiRequest": {
                                "transactionId": transaction_id,
                                "sessionStatus": "ACKNOWLEDGED",
                            },
                            "error": {
                                "code": 1000,
                                "message": "Patient consent record not found",
                            },
                            "resp": {"requestId": request_id},
                        }
                    ),
                    headers={
                        "X-CM-ID": os.environ["X-CM-ID"],
                        "Authorization": f"Bearer {gateway_access_token}",
                    },
                )
                logging.debug("Request acknowledged")
                logging.debug(f"{resp_code=}")
                return {
                    "status": "failed",
                    "details": "Patient consent record not found",
                }
        except Exception as error:
            logging.error(
                f"Error in DataTransferController.data_request function: {error}"
            )
            raise error

    def send_data_transfer_ack(self, request):
        try:
            consent_id = request["consent_id"]
            transaction_id = request["transaction_id"]
            hip_id = request["hip_id"]
            care_context_ack = request["care_context_ack"]
            request_id = request["request_id"]
            ack_request_id = str(uuid.uuid1())
            time_now = datetime.now(timezone.utc)
            time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            gateway_url = os.environ["gateway_url"]
            data_transfer_success_url = f"{gateway_url}/v0.5/health-information/notify"
            ack_request = {
                "requestId": ack_request_id,
                "timestamp": time_now,
                "notification": {
                    "consentId": consent_id,
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
                "Content-Type": "application/json",
            }
            _, ack_resp_code = APIInterface().post(
                route=data_transfer_success_url,
                data=json.dumps(ack_request),
                headers=headers,
            )
            print(f"ack sent {ack_resp_code=}")
            gateway_request = {"request_id": request_id}
            if ack_resp_code <= 250:
                gateway_request.update({"request_status": "SUCCESS"})
            else:
                gateway_request.update({"request_status": "FAILED"})
            CRUDGatewayInteraction().update(**gateway_request)
            return gateway_request
        except Exception as error:
            logging.error(
                f"Error in DataTransferController.send_data_transfer_ack function: {error}"
            )
            raise error
