from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from core.crud.hims_patientDetails_crud import CRUDPatientDetails
from core.crud.hims_patientMedicalRecord_crud import CRUDPatientMedicalRecord
from core import logger
from datetime import datetime, timezone, timedelta
import os
import uuid

logging = logger(__name__)


class CallbackController:
    def __init__(self):
        self.CRUDGatewayInteraction = CRUDGatewayInteraction()
        self.CRUDPatientDetails = CRUDPatientDetails()
        self.CRUDPatientMedicalRecord = CRUDPatientMedicalRecord()

    def on_fetch_modes(self, request):
        """[Controller to fetch patient auth modes]

        Args:
            request ([dict]): [fetch auth modes request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing  on_fetch_modes function")
            logging.info("Getting request id")
            request_id = request.get("resp").get("requestId")
            logging.info("Getting error message")
            error_message = request.get("error")
            logging.info(f"{error_message=}")
            if error_message:
                gateway_request = {
                    "request_id": request_id,
                    "callback_response": request,
                    "request_status": "FAILED",
                    "error_code": error_message.get("code", 000),
                    "error_message": error_message.get("message", None),
                }
            else:
                gateway_request = {
                    "request_id": request_id,
                    "callback_response": request,
                    "request_status": "SUCESS",
                }
            self.CRUDGatewayInteraction.update(**gateway_request)
            return {"status": "trigger success"}
        except Exception as error:
            logging.error(
                f"Error in CallbackController.on_fetch_modes function: {error}"
            )
            raise error

    def on_auth_init(self, request):
        try:
            logging.info("executing  on_auth_init function")
            logging.info("Getting request id")
            request_id = request.get("resp").get("requestId")
            logging.info("Getting error message")
            error_message = request.get("error")
            logging.info(f"{error_message=}")
            if error_message:
                gateway_request = {
                    "request_id": request_id,
                    "callback_response": request,
                    "request_status": "FAILED",
                    "error_code": error_message.get("code", 000),
                    "error_message": error_message.get("message", None),
                }
            else:
                gateway_request = {
                    "request_id": request_id,
                    "transaction_id": request.get("auth").get("transactionId"),
                    "callback_response": request,
                    "request_status": "SUCESS",
                }
            self.CRUDGatewayInteraction.update(**gateway_request)
            return {"status": "trigger success"}
        except Exception as error:
            logging.error(f"Error in CallbackController.on_auth_init function: {error}")
            raise error

    def on_auth_confirm(self, request, hip_id):
        try:
            logging.info("executing  on_auth_confirm function")
            logging.info("Getting Transcation id")
            request_id = request.get("resp").get("requestId")
            logging.info("Getting error message")
            error_message = request.get("error")
            logging.info(f"{error_message=}")
            if error_message:
                gateway_request = {
                    "request_id": request_id,
                    "callback_response": request,
                    "request_status": "FAILED",
                    "error_code": error_message.get("code", 000),
                    "error_message": error_message.get("message", None),
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
            else:
                # gateway_request = {
                #     "request_id": request_id,
                #     "callback_response": request,
                #     "request_status": "SUCESS",
                # }
                # self.CRUDGatewayInteraction.update(**gateway_request)
                logging.info("Creating patient record")
                access_token = request.get("auth").get("accessToken")
                patient_data = request.get("auth").get("patient")
                abha_number, mobile_number = None, None
                for idf in request.get("auth").get("patient").get("identifiers"):
                    if idf["type"] == "MOBILE":
                        mobile_number = idf["value"]
                    elif idf["type"] == "HEALTH_NUMBER":
                        abha_number = idf["value"].replace("-", "")
                patient_obj = self.CRUDPatientDetails.read_by_abhaId(
                    abha_number=abha_number, hip_id=hip_id
                )
                logging.info(f"{patient_data=}")
                address_obj = patient_data.get("address")
                if address_obj is None:
                    address_obj = {}
                logging.info(f"{patient_obj=}")
                patient_id = f"C360-PID-{str(uuid.uuid1().int)[:18]}"
                time_now = datetime.now()
                token_validity = time_now + timedelta(minutes=1440)
                token_validity = token_validity.strftime("%m/%d/%Y, %H:%M:%S")
                patient_request = {
                    "id": patient_id,
                    "abha_number": abha_number,
                    "abha_address": patient_data.get("id"),
                    "mobile_number": mobile_number,
                    "name": patient_data.get("name"),
                    "gender": patient_data.get("gender"),
                    "DOB": f"{patient_data.get('dayOfBirth')}/{patient_data.get('monthOfBirth')}/{patient_data.get('yearOfBirth')}",
                    "address": address_obj.get("line"),
                    "district": address_obj.get("district"),
                    "pincode": address_obj.get("state"),
                    "state_name": address_obj.get("pincode"),
                    "auth_methods": {"authMethods": ["AADHAAR_OTP", "MOBILE_OTP"]},
                    "hip_id": hip_id,
                    "access_token": {
                        "value": access_token,
                        "valid_till": token_validity,
                    },
                    "abha_status": "ACTIVE",
                }
                if patient_obj:
                    patient_request.update({"id": patient_obj["id"]})
                    self.CRUDPatientDetails.update(**patient_request)
                else:
                    self.CRUDPatientDetails.create(**patient_request)
                patient_obj_created = self.CRUDPatientDetails.read_by_abhaId(
                    abha_number=abha_number, hip_id=hip_id
                )
                if patient_obj_created:
                    pid = patient_obj_created["id"]
                    request.update({"patient_id": pid})
                gateway_request = {
                    "request_id": request_id,
                    "callback_response": request,
                    "request_status": "SUCESS",
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
                return patient_request
            return {"status": "trigger success"}
        except Exception as error:
            logging.error(
                f"Error in CallbackController.on_auth_confirm function: {error}"
            )
            raise error

    def on_add_context(self, request, hip_id):
        try:
            logging.info("executing  on_add_context function")
            logging.info("Getting Transcation id")
            request_id = request.get("resp").get("requestId")
            logging.info("Getting error message")
            error_message = request.get("error")
            logging.info(f"{error_message=}")
            if error_message:
                gateway_request = {
                    "request_id": request_id,
                    "callback_response": request,
                    "request_status": "FAILED",
                    "error_code": error_message.get("code", 000),
                    "error_message": error_message.get("message", None),
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
            else:
                gateway_obj = self.CRUDGatewayInteraction.read(request_id=request_id)
                gateway_metadata = gateway_obj.get("gateway_metadata")
                logging.info(f"{gateway_metadata=}")
                pmr_request = {
                    "id": gateway_metadata.get("pmr_id"),
                    "abdm_linked": True,
                }
                logging.info(f"{pmr_request=}")
                self.CRUDPatientMedicalRecord.update(**pmr_request)
                gateway_request = {
                    "request_id": request_id,
                    "callback_response": request,
                    "request_status": "SUCESS",
                }
                self.CRUDGatewayInteraction.update(**gateway_request)

            return {"status": "trigger success"}
        except Exception as error:
            logging.error(
                f"Error in CallbackController.on_add_context function: {error}"
            )
            raise error
