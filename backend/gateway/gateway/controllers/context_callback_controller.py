from gateway.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from gateway.crud.hims_patientMedicalRecord_crud import CRUDPatientMedicalRecord
from gateway import logger
from datetime import datetime, timezone
import os
import uuid

logging = logger(__name__)


class ContextCallbackController:
    def __init__(self):
        self.CRUDGatewayInteraction = CRUDGatewayInteraction()
        self.CRUDPatientMedicalRecord = CRUDPatientMedicalRecord()

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
