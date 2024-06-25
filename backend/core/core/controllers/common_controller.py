from core.crud.hims_docDetails_crud import CRUDDocDetails
from fastapi import APIRouter, HTTPException, status, Depends
from core.utils.custom.external_call import APIInterface
from core.utils.custom.session_helper import get_session_token
from core.controllers.users_controller import UserManagementController
from core.crud.hims_hip_crud import CRUDHIP

from core import logger
from datetime import datetime, timezone, timedelta
import uuid
import os, json


logging = logger(__name__)


class Common:
    def __init__(self):
        self.abha_url = os.environ["abha_url"]
        self.s3_location = os.environ["s3_location"]
        self.gateway_url = os.environ["gateway_url"]
        self.CRUDDocDetails = CRUDDocDetails()
        self.CRUDHIP = CRUDHIP()

    def abha_availability(self, health_id: str):
        """Verify if the abha address already exists
        Args:
            health_id (str): abha address to be checked
        Raises:
            HTTPException: _description_
            error: _description_
        Returns:
            _type_: _description_
        """
        try:
            logging.info("executing  abha_availability function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            verify_abha_url = f"{self.abha_url}/v2/search/existsByHealthId"
            resp, resp_code = APIInterface().post(
                route=verify_abha_url,
                data=json.dumps({"healthId": health_id}),
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            available_status = resp.get("status")
            logging.info(f"{available_status=}")
            if resp_code <= 250:
                if resp.get("status") == True:
                    return {"available": False}
                return {"available": True}
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=resp,
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except Exception as error:
            logging.error(f"Error in HIDController.abha_availability function: {error}")
            raise error

    def deep_link_notify(self, mobile_no: str, hip_id: str, hip_name: str):
        """Verify if the abha address already exists
        Args:
            health_id (str): abha address to be checked
        Raises:
            HTTPException: _description_
            error: _description_
        Returns:
            _type_: _description_
        """
        try:
            logging.info("executing  deep_link_notify function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            deep_link_request_id = str(uuid.uuid1())
            time_now = datetime.now(timezone.utc)
            time_now = time_now + timedelta(seconds=300)
            time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
            deep_link_url = f"{self.gateway_url }/v0.5/patients/sms/notify2"
            resp, resp_code = APIInterface().post(
                route=deep_link_url,
                data=json.dumps(
                    {
                        "requestId": deep_link_request_id,
                        "timestamp": time_now,
                        "notification": {
                            "phoneNo": f"+91-{mobile_no}",
                            "hip": {
                                "name": hip_name,
                                "id": hip_id,
                            },
                        },
                    }
                ),
                headers={
                    "Authorization": f"Bearer {gateway_access_token}",
                    "Content-Type": "application/json",
                    "X-CM-ID": os.environ["X-CM-ID"],
                },
            )
            if resp_code <= 250:
                return {"available": True}
            else:
                raise HTTPException(
                    status_code=resp_code,
                    detail=resp,
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except Exception as error:
            logging.error(f"Error in HIDController.deep_link_notify function: {error}")
            raise error

    def get_all_doctors(self, hip_id: str):
        """[Controller to get all Doctors records]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing get all Doctors function")
            logging.info(f"Getting the Doctors records")
            doc = self.CRUDDocDetails.read_by_hipId(hip_id=hip_id)
            logging.info(doc)
            return doc
        except Exception as error:
            logging.error(
                f"Error in CommonController.get_all_doctors function: {error}"
            )
            raise error

    def doctor_details_by_docId(self, doc_id: str):
        """[Controller to get all Doctors records]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing doctor_details_by_docId function")
            logging.info(f"Getting the Doctors records")
            doc_details = self.CRUDDocDetails.read_by_docId(doc_id=doc_id)
            logging.info(doc_details)
            return doc_details
        except Exception as error:
            logging.error(
                f"Error in CommonController.doctor_details_by_docId function: {error}"
            )
            raise error

    def create_doctor(self, request):
        try:
            logging.info("Creating doctor record")
            # for patient_obj in request.data:
            doctor_obj_dict = request.dict()
            logging.info(f"{doctor_obj_dict=}")
            doc_id = self.CRUDDocDetails.create(**doctor_obj_dict)
            return {"doc_id": doc_id}
        except Exception as error:
            logging.error(f"Error in Common.create_doctor function: {error}")
            raise error

    def check_endpoint_availability(self, endpoint):
        try:
            logging.info("executing check_endpoint_availability function")
            doctor_details_obj = self.CRUDDocDetails.read_by_uid(uid=endpoint)
            if doctor_details_obj:
                return {
                    "endpoint": endpoint,
                    "availability": False,
                    "doc_details": doctor_details_obj,
                }
            else:
                return {"endpoint": endpoint, "availability": True, "doc_details": {}}
        except Exception as error:
            logging.error(
                f"Error in Common.check_endpoint_availability function: {error}"
            )
            raise error

    def get_doctor_profile_details(self, endpoint):
        try:
            logging.info("executing get_doctor_profile_details function")
            doctor_details_obj = self.CRUDDocDetails.read_by_uid(uid=endpoint)
            if doctor_details_obj:
                return doctor_details_obj
            else:
                return {}
        except Exception as error:
            logging.error(
                f"Error in Common.get_doctor_profile_details function: {error}"
            )
            raise error

    def v2_create_doctor(self, request):
        try:
            logging.info("executing v2_create_doctor function")
            request_dict = request.dict()
            logging.info(f"{request_dict=}")
            logging.info("Creating user signup request")
            doc_first_name = request_dict.pop("doc_first_name")
            doc_last_name = request_dict.pop("doc_last_name")
            user_signup_request = {
                "mobile_number": request_dict.get("mobile_number"),
                "password": request_dict.pop("password"),
                "name": f"Dr. {doc_first_name} {doc_last_name}",
                "email_id": request_dict.get("email_id"),
            }
            logging.info(f"{user_signup_request=}")
            registered_user_obj = UserManagementController().register_user_controller(
                request=user_signup_request
            )
            logging.info(f"{registered_user_obj=}")
            hip_details = self.CRUDHIP.read(hip_ip=request_dict.get("hip_id"))
            logging.info("Creating user onboard request")
            user_onboard_request = {
                "mobile_number": request_dict.get("mobile_number"),
                "hip_name": hip_details.get("name"),
                "hip_id": request_dict.get("hip_id"),
                "user_role": request_dict.pop("user_role"),
                "department": request_dict.get("doc_department"),
            }
            logging.info(f"{user_onboard_request=}")
            UserManagementController().onboard_user_controller(
                request=user_onboard_request,
            )
            logging.info("Creating doc_uid")
            # doc_uid = f"dr-{doc_first_name.lower()}-{doc_last_name.lower()}-{request_dict.get('doc_specialization')}-{hip_details.get('hip_city')}"
            # logging.info(f"{doc_uid=}")
            request_dict.update({"doc_name": f"Dr. {doc_first_name} {doc_last_name}"})
            # request_dict.update({"doc_uid": doc_uid})
            logging.info(f"{request_dict=}")
            doc_details_obj = self.CRUDDocDetails.read_by_mobile_number(
                mobile_number=request_dict.get("mobile_number")
            )
            if doc_details_obj:
                logging.info("Doctor Already exists")
                doc_details_obj.update(
                    {"status": "Doctor already exists with provided mobile number"}
                )
            else:
                doc_details_obj = self.CRUDDocDetails.create(**request_dict)
                doc_details_obj.update({"status": "New Doctor created successfully"})
            return doc_details_obj
        except Exception as error:
            logging.error(f"Error in Common.v2_create_doctor function: {error}")
            raise error

    def update_doc_details(self, request):
        try:
            logging.info("Updating doctor details records")
            # for patient_obj in request.data:
            doctor_obj_dict = request.dict()
            doctor_obj_dict.pop("doc_id")
            self.CRUDDocDetails.update(**doctor_obj_dict, id=request.doc_id)
            return {"doc_id": request.doc_id}
        except Exception as error:
            logging.error(f"Error in Common.update_doctor function: {error}")
            raise error
