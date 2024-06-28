from core.crud.hims_docDetails_crud import CRUDDocDetails
from core.controllers.users_controller import UserManagementController
from core.crud.hims_hip_crud import CRUDHIP
from core import logger
from core.apis.schemas.requests.user_request import (
    Register,
    OnBoard,
)


logging = logger(__name__)


class DoctorController:
    def __init__(self):
        self.CRUDDocDetails = CRUDDocDetails()
        self.CRUDHIP = CRUDHIP()

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
                f"Error in DoctorController.get_all_doctors function: {error}"
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
                f"Error in DoctorController.doctor_details_by_docId function: {error}"
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
            logging.error(f"Error in DoctorController.create_doctor function: {error}")
            raise error

    def check_endpoint_availability(self, endpoint):
        try:
            logging.info("executing check_endpoint_availability function")
            doctor_details_obj = self.CRUDDocDetails.read_by_uid(uid=endpoint)
            if doctor_details_obj:
                return {"endpoint": endpoint, "availability": False}
            else:
                return {"endpoint": endpoint, "availability": True}
        except Exception as error:
            logging.error(
                f"Error in DoctorController.check_endpoint_availability function: {error}"
            )
            raise error

    def get_doctor_profile_details(self, endpoint):
        try:
            logging.info("executing get_doctor_profile_details function")
            doctor_details_obj = self.CRUDDocDetails.read_by_uid(uid=endpoint)
            if doctor_details_obj:
                hip_details = self.CRUDHIP.read(hip_ip=doctor_details_obj.get("hip_id"))
                doctor_details_obj.update({"primary_hip": [hip_details]})
            return doctor_details_obj
        except Exception as error:
            logging.error(
                f"Error in DoctorController.get_doctor_profile_details function: {error}"
            )
            raise error

    def v2_create_doctor(self, request):
        try:
            logging.info("executing v2_create_doctor function")
            request_dict = request.dict()
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
                registered_user_obj = (
                    UserManagementController().register_user_controller(
                        request=Register(**user_signup_request)
                    )
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
                    request=OnBoard(**user_onboard_request),
                )
                request_dict.update(
                    {"doc_name": f"Dr. {doc_first_name} {doc_last_name}"}
                )
                logging.info(f"{request_dict=}")
                doc_details_obj = self.CRUDDocDetails.create(**request_dict)
                doc_details_obj.update({"status": "New Doctor created successfully"})
            return doc_details_obj
        except Exception as error:
            logging.error(
                f"Error in DoctorController.v2_create_doctor function: {error}"
            )
            raise error

    def update_doc_details(self, request):
        try:
            logging.info("Updating doctor details records")
            request_dict = request.dict()
            doc_first_name = request_dict.pop("doc_first_name")
            doc_last_name = request_dict.pop("doc_last_name")
            if doc_first_name and doc_last_name:
                request_dict.update(
                    {"doc_name": f"Dr. {doc_first_name} {doc_last_name}"}
                )
            logging.info(f"{request_dict=}")
            cleaned_data = {k: v for k, v in request_dict.items() if v is not None}
            self.CRUDDocDetails.update(**cleaned_data)
            return {"doc_id": request_dict.get("id")}
        except Exception as error:
            logging.error(f"Error in DoctorController.update_doctor function: {error}")
            raise error

    def update_profile_photo_signature(self, request):
        try:
            logging.info("executing update_profile_photo_signature function")
            self.CRUDDocDetails.update(**request)
            logging.info(f"{request=}")
            return {"doc_id": request.get("id")}
        except Exception as error:
            logging.error(
                f"Error in DoctorController.update_profile_photo_signature function: {error}"
            )
            raise error
