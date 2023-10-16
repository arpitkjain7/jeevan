from core.crud.hims_docDetails_crud import CRUDDocDetails
from core.crud.hims_template_crud import CRUDTemplate
from fastapi import APIRouter, HTTPException, status, Depends
from core.utils.custom.external_call import APIInterface
from core.utils.custom.session_helper import get_session_token
from commons.auth import encrypt_password, verify_hash_password, signJWT
from core import logger
import os

logging = logger(__name__)


class Common:
    def __init__(self):
        self.abha_url = os.environ["abha_url"]
        self.s3_location = os.environ["s3_location"]
        self.gateway_url = os.environ["gateway_url"]
        self.CRUD_docDetails = CRUDDocDetails()
        self.CRUDTemplate = CRUDTemplate()

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
                data={"healthId": health_id},
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

    def deep_link_notify(self, mobile_no: str):
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
            deep_link_url = f"{self.gateway_url }/v0.5/patients/sms/notify"
            resp, resp_code = APIInterface().post(
                route=deep_link_url,
                data={
                    {
                        "requestId": "{{$guid}}",
                        "timestamp": "2023-05-27T08:41:55Z",
                        "notification": {
                            "phoneNo": "+91-9511878113",
                            "hip": {
                                "name": "Max Healthcare",
                                "id": "ABCABC",
                            },
                        },
                    }
                },
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
            doc = self.CRUD_docDetails.read_by_hipId(hip_id=hip_id)
            logging.info(doc)
            return doc
        except Exception as error:
            logging.error(
                f"Error in CommonController.get_all_doctors function: {error}"
            )
            raise error

    def create_doctor(self, request):
        try:
            logging.info("Creating doctor record")
            # for patient_obj in request.data:
            doctor_obj_dict = request.dict()
            logging.info(f"{doctor_obj_dict=}")
            doc_id = self.CRUD_docDetails.create(**doctor_obj_dict)
            return {"doc_id": doc_id}
        except Exception as error:
            logging.error(f"Error in Common.create_doctor function: {error}")
            raise error

    def update_doc_details(self, request):
        try:
            logging.info("Updating doctor details records")
            # for patient_obj in request.data:
            doctor_obj_dict = request.dict()
            doctor_obj_dict.pop("doc_id")
            self.CRUD_docDetails.update(**doctor_obj_dict, id=request.doc_id)
            return {"doc_id": request.doc_id}
        except Exception as error:
            logging.error(f"Error in Common.update_doctor function: {error}")
            raise error

    def create_template(self, request, doc_id):
        try:
            logging.info("Creating template record")
            # for patient_obj in request.data:
            template_obj_dict = request.dict()
            template_obj_dict.update({"doc_id": doc_id})
            logging.info(f"{template_obj_dict=}")
            template_id = self.CRUDTemplate.create(**template_obj_dict)
            return {"template_id": template_id}
        except Exception as error:
            logging.error(f"Error in Common.create_template function: {error}")
            raise error

    def get_template_by_id(self, template_id):
        try:
            logging.info("Creating template record")
            # for patient_obj in request.data:
            logging.info(f"{template_id=}")
            template_obj = self.CRUDTemplate.read_by_template_id(
                template_id=template_id
            )
            return template_obj
        except Exception as error:
            logging.error(f"Error in Common.get_template_by_id function: {error}")
            raise error

    def get_template_by_type(self, name, type, doc_id):
        try:
            logging.info("Get template record")
            # for patient_obj in request.data:
            logging.info(f"{name=}")
            logging.info(f"{type=}")
            if name is not None:
                template_obj = self.CRUDTemplate.read_by_name(name=name, doc_id=doc_id)
            elif type is not None:
                template_obj = self.CRUDTemplate.read_by_type(type=type, doc_id=doc_id)
            logging.info(f"{template_obj=}")
            return template_obj
        except Exception as error:
            logging.error(f"Error in Common.get_template_by_type function: {error}")
            raise error

    def get_all_template(self, doc_id):
        try:
            logging.info("Creating template record")
            # for patient_obj in request.data:
            template_obj = self.CRUDTemplate.read_all(doc_id=doc_id)
            return {"template_obj": template_obj}
        except Exception as error:
            logging.error(f"Error in Common.get_all_template function: {error}")
            raise error
