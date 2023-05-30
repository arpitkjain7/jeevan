from core.crud.hims_patientDetails_crud import CRUDPatientDetails
from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from core.crud.hims_hip_crud import CRUDHIP
from core.crud.hims_patientMedicalRecord_crud import CRUDPatientMedicalRecord
from core.crud.hims_consent_crud import CRUDConsents
from core.utils.custom.data_transfer_helper import send_data
from core.utils.custom.external_call import APIInterface
from core.utils.custom.session_helper import get_session_token
from core import logger
from datetime import datetime, timezone
import os
import uuid
from pytz import timezone as pytz_timezone
from core import celery
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

    def consent_notify(self, request):
        try:
            logging.info("executing  consent_notify function")
            logging.info("Creating gateway record")
            notification_obj = request.get("notification")
            consent_status = notification_obj.get("status")
            consent_id = notification_obj.get("consentId")
            consent_details = notification_obj.get("consentDetail")
            request_id = request.get("requestId")
            if consent_status == "GRANTED":
                logging.info("Consent granted")
                crud_request = {
                    "request_id": request_id,
                    "request_type": "CONSENT_NOTIFY_GRANT",
                    "request_status": "PROCESSING",
                    "transaction_id": consent_id,
                    "callback_response": consent_details,
                }
                self.CRUDGatewayInteraction.create(**crud_request)
                logging.info("Creating consent table record")
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
                logging.info("Consent expired or revoked")
                crud_request = {
                    "request_id": request_id,
                    "request_type": "CONSENT_NOTIFY_EXPIRE",
                    "request_status": "PROCESSING",
                    "transaction_id": consent_id,
                    "callback_response": consent_details,
                }
                self.CRUDGatewayInteraction.create(**crud_request)
                logging.info("Creating consent table record")
                consent_crud_request = {"id": consent_id, "status": consent_status}
                self.CRUDConsents.update(**consent_crud_request)
            logging.info("Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            consent_on_notify_url = f"{self.gateway_url}/v0.5/consents/hip/on-notify"
            notify_request_id = str(uuid.uuid1())
            time_now = datetime.now(timezone.utc)
            time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S")
            _, resp_code = APIInterface().post(
                route=consent_on_notify_url,
                data={
                    "requestId": notify_request_id,
                    "timestamp": time_now,
                    "acknowledgement": {
                        "status": "OK",
                        "consentId": consent_id,
                    },
                    "resp": {"requestId": request_id},
                },
                headers={
                    "X-CM-ID": "sbx",
                    "Authorization": f"Bearer {gateway_access_token}",
                },
            )
            logging.debug(f"{resp_code=}")
            gateway_request = {"request_id": request_id}
            if resp_code <= 250:
                gateway_request.update({"request_status": "SUCCESS"})
            else:
                gateway_request.update({"request_status": "FAILED"})
            self.CRUDGatewayInteraction.update(**gateway_request)
            return gateway_request
        except Exception as error:
            logging.error(
                f"Error in DataTransferController.consent_notify function: {error}"
            )
            raise error


@celery.task
def data_request(request):
    try:
        logging.info("executing  data_request function")
        logging.info("Creating gateway record")
        transaction_id = request.get("transactionId")
        request_id = request.get("requestId")
        hi_request_obj = request.get("hiRequest")
        consent_id = hi_request_obj.get("consent").get("id")
        consent_obj = CRUDConsents().read(consent_id=consent_id)
        gateway_url = os.environ["gateway_url"]
        consent_on_notify_url = f"{gateway_url}/v0.5/health-information/hip/on-request"
        time_now = datetime.now(timezone.utc)
        logging.info(f"{time_now=}")
        expire_datetime_object = parser.parse(consent_obj.get("expire_at"))
        logging.info(f"{expire_datetime_object=}")
        utc_timezone = pytz_timezone("UTC")
        logging.info(f"{utc_timezone=}")
        expire_time_utc = utc_timezone.localize(expire_datetime_object)
        logging.info(f"{expire_time_utc=}")
        expire_time = expire_datetime_object.strftime("%Y-%m-%dT%H:%M:%S")
        logging.info(f"{expire_time=}")
        if time_now < expire_time_utc and consent_obj.get("status") == "GRANTED":
            crud_request = {
                "request_id": request_id,
                "request_type": "DATA_REQUEST",
                "request_status": "PROCESSING",
                "transaction_id": transaction_id,
                "callback_response": hi_request_obj,
            }
            CRUDGatewayInteraction().create(**crud_request)
            logging.info("Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            consent_on_notify_url = (
                f"{gateway_url}/v0.5/health-information/hip/on-request"
            )
            notify_request_id = str(uuid.uuid1())
            time_now = datetime.now(timezone.utc)
            time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S")
            _, resp_code = APIInterface().post(
                route=consent_on_notify_url,
                data={
                    "requestId": notify_request_id,
                    "timestamp": time_now,
                    "hiRequest": {
                        "transactionId": transaction_id,
                        "sessionStatus": "ACKNOWLEDGED",
                    },
                    "resp": {"requestId": request_id},
                },
                headers={
                    "X-CM-ID": "sbx",
                    "Authorization": f"Bearer {gateway_access_token}",
                },
            )
            logging.debug("Request acknowledged")
            logging.debug(f"{resp_code=}")
            hi_request = request.get("hiRequest")
            logging.debug("preparing data as background task")
            logging.info(f"{hi_request=},{consent_id=},{transaction_id=},{request_id=}")
            send_data(
                hi_request=request.get("hiRequest"),
                consent_obj=consent_obj,
                transaction_id=transaction_id,
                request_id=request_id,
            )
            return {"status": "success"}
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
                data={
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
                },
                headers={
                    "X-CM-ID": "sbx",
                    "Authorization": f"Bearer {gateway_access_token}",
                },
            )
            logging.debug("Request acknowledged")
            logging.debug(f"{resp_code=}")
            return {"status": "success"}
    except Exception as error:
        logging.error(f"Error in DataTransferController.data_request function: {error}")
        raise error
