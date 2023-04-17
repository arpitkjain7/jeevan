from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from core.crud.hims_patientDetails_crud import CRUDPatientDetails
from core import logger
from datetime import datetime, timezone
import os
import uuid

logging = logger(__name__)


class CallbackController:
    def __init__(self):
        self.CRUDGatewayInteraction = CRUDGatewayInteraction()
        self.CRUDPatientDetails = CRUDPatientDetails()

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

    def on_auth_confirm(self, request):
        try:
            logging.info("executing  on_auth_confirm function")
            logging.info("Getting request id")
            request_id = request.get("resp").get("requestId")
            logging.info("Getting error message")
            error_message = request.get("error")
            logging.info(f"{error_message=}")
            if error_message:
                gateway_request = {
                    "request_id": request.get("resp").get("requestId"),
                    "callback_response": request,
                    "request_status": "FAILED",
                    "error_code": error_message.get("code", 000),
                    "error_message": error_message.get("message", None),
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
            else:
                gateway_request = {
                    "request_id": request.get("resp").get("requestId"),
                    "callback_response": request,
                    "request_status": "SUCESS",
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
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
                    abha_number=abha_number
                )
                patient_id = str(uuid.uuid1())
                patient_request = {
                    "id": patient_id,
                    "abha_number": abha_number,
                    "abha_address": patient_data.get("id"),
                    "mobile_number": mobile_number,
                    "name": patient_data.get("name"),
                    "gender": patient_data.get("gender"),
                    "DOB": f"{patient_data.get('dayOfBirth')}/{patient_data.get('monthOfBirth')}/{patient_data.get('yearOfBirth')}",
                    "address": patient_data.get("address").get("line"),
                    "district": patient_data.get("address").get("district"),
                    "pincode": patient_data.get("address").get("state"),
                    "state_name": patient_data.get("address").get("pincode"),
                    "access_token": access_token,
                }
                if patient_obj:
                    patient_request.update({"id": patient_obj["id"]})
                    self.CRUDPatientDetails.update(**patient_request)
                else:
                    self.CRUDPatientDetails.create(**patient_request)
                return patient_request
            return {"status": "trigger success"}
        except Exception as error:
            logging.error(
                f"Error in CallbackController.on_auth_confirm function: {error}"
            )
            raise error
