from core.crud.hims_patientDetails_crud import CRUDPatientDetails
from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from core.utils.custom.external_call import APIInterface
from core.utils.custom.session_helper import get_session_token
from core import logger
from datetime import datetime, timezone
import os
import uuid

logging = logger(__name__)


class PatientController:
    def __init__(self):
        self.CRUDPatientDetails = CRUDPatientDetails()
        self.CRUDGatewayInteraction = CRUDGatewayInteraction()
        self.gateway_url = os.environ["gateway_url"]

    def fetch_auth_modes(self, request, hip_id):
        """[Controller to fetch patient auth modes]

        Args:
            request ([dict]): [fetch auth modes request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing  fetch_auth_modes function")
            request_dict = request.dict()
            logging.info("Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            fetch_modes_url = f"{self.gateway_url}/v0.5/users/auth/fetch-modes"
            request_id = str(uuid.uuid1())
            time_now = datetime.now(timezone.utc)
            time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
            _, resp_code = APIInterface().post(
                route=fetch_modes_url,
                data={
                    "requestId": request_id,
                    "timestamp": time_now,
                    "query": {
                        "id": request_dict.get("abha_number"),
                        "purpose": request_dict.get("purpose"),
                        "requester": {"type": "HIP", "id": hip_id},
                    },
                },
                headers={
                    "X-CM-ID": "sbx",
                    "Authorization": f"Bearer {gateway_access_token}",
                },
            )
            logging.debug(f"{resp_code=}")
            gateway_request = {
                "request_id": request_id,
                "request_type": "FETCH_AUTH_MODE",
            }
            if resp_code <= 250:
                gateway_request.update({"request_status": "PROCESSING"})
            else:
                gateway_request.update({"request_status": "FAILED"})
            self.CRUDGatewayInteraction.create(**gateway_request)
            gateway_request.update({"txn_id": request_id})
            return gateway_request
        except Exception as error:
            logging.error(
                f"Error in PatientController.fetch_auth_modes function: {error}"
            )
            raise error

    def auth_init(self, request, hip_id):
        try:
            logging.info("executing  auth_init function")
            request_dict = request.dict()
            logging.info("Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            fetch_modes_url = f"{self.gateway_url}/v0.5/users/auth/init"
            request_id = str(uuid.uuid1())
            time_now = datetime.now(timezone.utc)
            time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
            _, resp_code = APIInterface().post(
                route=fetch_modes_url,
                data={
                    "requestId": request_id,
                    "timestamp": time_now,
                    "query": {
                        "id": request_dict.get("abha_number"),
                        "purpose": request_dict.get("purpose"),
                        "authMode": request_dict.get("auth_mode"),
                        "requester": {"type": "HIP", "id": hip_id},
                    },
                },
                headers={
                    "X-CM-ID": "sbx",
                    "Authorization": f"Bearer {gateway_access_token}",
                },
            )
            logging.debug(f"{resp_code=}")
            gateway_request = {
                "request_id": request_id,
                "request_type": "AUTH_INIT",
            }
            if resp_code <= 250:
                gateway_request.update({"request_status": "PROCESSING"})
            else:
                gateway_request.update({"request_status": "FAILED"})
            self.CRUDGatewayInteraction.create(**gateway_request)
            gateway_request.update({"txn_id": request_id})
            return gateway_request
        except Exception as error:
            logging.error(f"Error in PatientController.auth_init function: {error}")
            raise error

    def verify_otp(self, request):
        try:
            logging.info("executing  verify_otp function")
            request_dict = request.dict()
            logging.info("Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            auth_confirm_url = f"{self.gateway_url}/v0.5/users/auth/confirm"
            gateway_obj = self.CRUDGatewayInteraction.read(
                request_id=request_dict.get("txnId")
            )
            request_id = str(uuid.uuid1())
            time_now = datetime.now(timezone.utc)
            time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
            resp, resp_code = APIInterface().post(
                route=auth_confirm_url,
                data={
                    "requestId": request_id,
                    "timestamp": time_now,
                    "transactionId": gateway_obj.get("transaction_id"),
                    "credential": {"authCode": request_dict.get("otp")},
                },
                headers={
                    "X-CM-ID": "sbx",
                    "Authorization": f"Bearer {gateway_access_token}",
                },
            )
            logging.debug(f"{resp_code=}")
            gateway_request = {
                "request_id": request_id,
                "request_type": "VERIFY_OTP",
            }
            if resp_code <= 250:
                gateway_request.update({"request_status": "PROCESSING"})
            else:
                gateway_request.update({"request_status": "FAILED"})
            self.CRUDGatewayInteraction.create(**gateway_request)
            return gateway_request
        except Exception as error:
            logging.error(f"Error in PatientController.verify_otp function: {error}")
            raise error

    def patient_share(self, request):
        try:
            logging.info("executing  patient_share function")
            logging.info("Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            patient_data = request.get("profile").get("patient")
            logging.info("Getting identifiers")
            for idf in patient_data.get("identifiers"):
                if idf["type"] == "MOBILE":
                    mobile_number = idf["value"]
                if idf["type"] == "EMAIL":
                    email_id = idf["value"]
            patient_obj = self.CRUDPatientDetails.read_by_abhaAddress(
                abha_address=patient_data.get("healthId")
            )
            if patient_obj is None:
                abha_number = patient_data.get("healthIdNumber")
                if abha_number:
                    abha_number = abha_number.replace("-", "")
                patient_id = str(uuid.uuid1())
                patient_request = {
                    "id": patient_id,
                    "abha_number": abha_number,
                    "abha_address": patient_data["healthId"],
                    "mobile_number": mobile_number,
                    "name": patient_data["name"],
                    "gender": patient_data["gender"],
                    "DOB": f"{patient_data['dayOfBirth']}/{patient_data['monthOfBirth']}/{patient_data['yearOfBirth']}",
                    "email": email_id,
                    "address": patient_data["address"]["line"],
                    "district": patient_data["address"]["district"],
                    "pincode": patient_data["address"]["pincode"],
                    "state_name": patient_data["address"]["state"],
                }
                self.CRUDPatientDetails.create(**patient_request)
            akw_url = f"{self.gateway_url}/v1.0/patients/profile/on-share"
            request_id = str(uuid.uuid1())
            time_now = datetime.now(timezone.utc)
            time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
            resp, resp_code = APIInterface().post(
                route=akw_url,
                data={
                    "requestId": request_id,
                    "timestamp": time_now,
                    "acknowledgement": {
                        "status": "SUCCESS",
                        "healthId": patient_data.get("healthId"),
                        "tokenNumber": "122",
                    },
                    "error": None,
                    "resp": {"requestId": request.get("requestId")},
                },
                headers={
                    "X-CM-ID": "sbx",
                    "Authorization": f"Bearer {gateway_access_token}",
                },
            )
            logging.debug(f"{resp_code=}")
            logging.debug(f"{resp=}")
            return {"status": resp_code, "statusText": resp, "data": resp}
        except Exception as error:
            logging.error(f"Error in PatientController.patient_share function: {error}")
            raise error
