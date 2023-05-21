from core.crud.hims_patientDetails_crud import CRUDPatientDetails
from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from core.crud.hims_hip_crud import CRUDHIP
from core.crud.hims_patientMedicalRecord_crud import CRUDPatientMedicalRecord
from core.utils.custom.data_transfer_helper import send_data
from core.utils.custom.external_call import APIInterface
from core.utils.custom.session_helper import get_session_token
from core import logger
from core.utils.custom.fuzzy_match import FuzzyMatch
from datetime import datetime, timezone, timedelta
import os
import uuid
from pytz import timezone as pytz_timezone

logging = logger(__name__)


class DataTransferController:
    def __init__(self):
        self.CRUDPatientDetails = CRUDPatientDetails()
        self.CRUDGatewayInteraction = CRUDGatewayInteraction()
        self.CRUDHIP = CRUDHIP()
        self.CRUDPatientMedicalRecord = CRUDPatientMedicalRecord()
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
                crud_request = {
                    "request_id": consent_id,
                    "request_type": "CONSENT_NOTIFY",
                    "request_status": "PROCESSING",
                    "transaction_id": request_id,
                    "callback_response": consent_details,
                }
                self.CRUDGatewayInteraction.create(**crud_request)
                logging.info("Getting session access Token")
                gateway_access_token = get_session_token(
                    session_parameter="gateway_token"
                ).get("accessToken")
                consent_on_notify_url = (
                    f"{self.gateway_url}/v0.5/consents/hip/on-notify"
                )
                logging.info("Iterating through the consent records")
                hip_id = consent_details.get("hip").get("id")
                consent_found = True
                # for consent_obj in consent_details.get("careContexts"):
                #     patient_id = consent_obj.get("patientReference")
                #     pmr_id = consent_obj.get("careContextReference")
                #     pmr_obj = self.CRUDPatientMedicalRecord.read(pmr_id=pmr_id)
                #     if pmr_obj is None:
                #         consent_found = False
                notify_request_id = str(uuid.uuid1())
                time_now = datetime.now(timezone.utc)
                time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
                if not consent_found:
                    error_obj = {
                        "error": {
                            "code": 1000,
                            "message": "Patient consent record not found",
                        },
                    }
                else:
                    error_obj = None
                _, resp_code = APIInterface().post(
                    route=consent_on_notify_url,
                    data={
                        "requestId": notify_request_id,
                        "timestamp": time_now,
                        "acknowledgement": {
                            "status": "OK",
                            "consentId": consent_id,
                        },
                        "error": error_obj,
                        "resp": {"requestId": request_id},
                    },
                    headers={
                        "X-CM-ID": "sbx",
                        "Authorization": f"Bearer {gateway_access_token}",
                    },
                )
                logging.debug(f"{resp_code=}")
                gateway_request = {"request_id": consent_id}
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

    def data_request(self, request):
        try:
            logging.info("executing  data_request function")
            logging.info("Creating gateway record")
            transaction_id = request.get("transactionId")
            request_id = request.get("requestId")
            consent_id = request.get("hiRequest").get("consent").get("id")
            gateway_obj = self.CRUDGatewayInteraction.read(request_id=request_id)
            if not gateway_obj:
                crud_request = {
                    "request_id": request_id,
                    "request_type": "DATA_REQUEST",
                    "request_status": "PROCESSING",
                    "transaction_id": transaction_id,
                    "callback_response": request.get("hiRequest"),
                }
                self.CRUDGatewayInteraction.create(**crud_request)
                logging.info("Getting session access Token")
                gateway_access_token = get_session_token(
                    session_parameter="gateway_token"
                ).get("accessToken")
                consent_on_notify_url = (
                    f"{self.gateway_url}/v0.5/health-information/hip/on-request"
                )
                notify_request_id = str(uuid.uuid1())
                time_now = datetime.now(timezone.utc)
                time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
                consent_obj = self.CRUDGatewayInteraction.read(request_id=consent_id)
                if consent_obj:
                    error_obj = None
                else:
                    error_obj = {
                        "error": {
                            "code": 1000,
                            "message": "Patient consent record not found",
                        },
                    }
                _, resp_code = APIInterface().post(
                    route=consent_on_notify_url,
                    data={
                        "requestId": notify_request_id,
                        "timestamp": time_now,
                        "hiRequest": {
                            "transactionId": transaction_id,
                            "sessionStatus": "ACKNOWLEDGED",
                        },
                        "error": error_obj,
                        "resp": {"requestId": request_id},
                    },
                    headers={
                        "X-CM-ID": "sbx",
                        "Authorization": f"Bearer {gateway_access_token}",
                    },
                )
                logging.debug(f"{resp_code=}")
                send_data(
                    hi_request=request.get("hiRequest"),
                    consent_obj=consent_obj,
                    transaction_id=transaction_id,
                )
                gateway_request = {"request_id": request_id}
                if resp_code <= 250:
                    gateway_request.update({"request_status": "SUCCESS"})
                else:
                    gateway_request.update({"request_status": "FAILED"})
                self.CRUDGatewayInteraction.update(**gateway_request)
                return gateway_request
            else:
                return {"status": "record already exists"}
        except Exception as error:
            logging.error(
                f"Error in DataTransferController.data_request function: {error}"
            )
            raise error
