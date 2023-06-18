from core.crud.hims_hip_crud import CRUDHIP
from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from core.crud.hims_docDetails_crud import CRUDDocDetails
from core import logger
from core.utils.custom.external_call import APIInterface
from core.utils.custom.session_helper import get_session_token
import os
import uuid
from datetime import datetime, timezone
from pytz import timezone as pytz_timezone
from dateutil import parser

logging = logger(__name__)


class HIUController:
    def __init__(self):
        self.CRUDHIP = CRUDHIP()
        self.CRUDGatewayInteraction = CRUDGatewayInteraction()
        self.CRUDDocDetails = CRUDDocDetails()
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
                    "X-CM-ID": "sbx",
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
        pass

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
                    "X-CM-ID": "sbx",
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
