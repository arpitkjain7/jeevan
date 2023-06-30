from core.crud.hims_listOfComplaints_crud import CRUDListOfComplaints
from core.crud.hims_listOfDiagnosis_crud import CRUDListOfDiagosis
from core.crud.hims_listOfMedicalTests_crud import CRUDListOfMedicalTests
from core.crud.hims_listOfMedicines_crud import CRUDListOfMedicines
from core.crud.hims_listOfPrecautions_crud import CRUDListOfPrecautions
from core.crud.hims_docDetails_crud import CRUDDocDetails
from fastapi import APIRouter, HTTPException, status, Depends
from core.utils.custom.external_call import APIInterface
from core.utils.custom.session_helper import get_session_token
from commons.auth import encrypt_password, verify_hash_password, signJWT
from core import logger
import os

logging = logger(__name__)


class ListOfComplaintsController:
    def __init__(self):
        self.CRUDListOfComplaints = CRUDListOfComplaints()

    def add_complaint_controller(self, complaint):
        """[Controller to register new user]

        Args:
            request ([dict]): [create new user request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing add new complaint function")
            complaint_lower = complaint.lower()
            complaint_obj = self.CRUDListOfComplaints.read(complaint=complaint_lower)
            if complaint_obj:
                complaint_obj.update({"status": "Complaint already exist"})
                return complaint_obj
            complaint_id = self.CRUDListOfComplaints.create(
                **{"complaint": complaint_lower}
            )
            return {
                "complaint_id": complaint_id,
                "complaint": complaint_lower,
                "status": "Complaint added successfully",
            }
        except Exception as error:
            logging.error(f"Error in create_complaint_controller function: {error}")
            raise error

    def get_all_complaints_controller(self):
        """[Controller to get all users]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [list]: [list of all the users in the system]
        """
        try:
            logging.info("executing get_all_complaints_controller function")
            complaint_list = self.CRUDListOfComplaints.read_all()
            return complaint_list
        except Exception as error:
            logging.error(f"Error in get_all_complaint_controller function: {error}")

    def delete_complaint_controller(self, complaint_id):
        """[Controller to delete a user]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [deleted user details]
        """
        try:
            logging.info("executing delete_complaint_controller function")
            response = self.CRUDListOfComplaints.delete(complaint_id=complaint_id)
            response.update({"status": "Complaint Deleted Successfully"})
            return response
        except Exception as error:
            logging.error(f"Error in delete_complaint_controller function: {error}")
            raise {"error": "Invalid username or password"}


class ListOfDiagnosisController:
    def __init__(self):
        self.CRUDListOfDiagnosis = CRUDListOfDiagosis()

    def add_disease_controller(self, disease):
        """[Controller to register new user]

        Args:
            request ([dict]): [create new user request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing add new complaint function")
            disease_upper = disease.upper()
            disease_obj = self.CRUDListOfDiagnosis.read(disease=disease_upper)
            if disease_obj:
                disease_obj.update({"status": "Disease already exist"})
                return disease_obj
            disease_id = self.CRUDListOfDiagnosis.create(**{"disease": disease_upper})
            return {
                "disease_id": disease_id,
                "disease": disease_upper,
                "status": "Disease added successfully",
            }
        except Exception as error:
            logging.error(f"Error in create_complaint_controller function: {error}")
            raise error

    def get_all_diseases_controller(self):
        """[Controller to get all users]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [list]: [list of all the users in the system]
        """
        try:
            logging.info("executing get_all_diseases_controller function")
            diseases_list = self.CRUDListOfDiagnosis.read_all()
            return diseases_list
        except Exception as error:
            logging.error(f"Error in get_all_complaint_controller function: {error}")

    def delete_disease_controller(self, disease_id):
        """[Controller to delete a user]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [deleted user details]
        """
        try:
            logging.info("executing delete_disease_controller function")
            response = self.CRUDListOfDiagnosis.delete(disease_id=disease_id)
            response.update({"status": "Disease Deleted Successfully"})
            return response
        except Exception as error:
            logging.error(f"Error in delete_diseases_controller function: {error}")
            raise {"error": "Invalid username or password"}


class ListOfMedicalTestsController:
    def __init__(self):
        self.CRUDListOfMedicalTests = CRUDListOfMedicalTests()

    def add_medicalTest_controller(self, medicalTest):
        """[Controller to register new user]

        Args:
            request ([dict]): [create new user request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing add new medical test function")
            medicalTest_upper = medicalTest.upper()
            medicalTest_obj = self.CRUDListOfMedicalTests.read(
                medical_test_name=medicalTest_upper
            )
            if medicalTest_obj:
                medicalTest_obj.update({"status": "Test already exist"})
                return medicalTest_obj
            medicalTest_id = self.CRUDListOfMedicalTests.create(
                **{"name": medicalTest_upper}
            )
            return {
                "medical_test_id": medicalTest_id,
                "medical_test": medicalTest_upper,
                "status": "Test added successfully",
            }
        except Exception as error:
            logging.error(f"Error in create_medical_test_controller function: {error}")
            raise error

    def get_all_tests_controller(self):
        """[Controller to get all users]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [list]: [list of all the users in the system]
        """
        try:
            logging.info("executing get_all_tests_controller function")
            tests_list = self.CRUDListOfMedicalTests.read_all()
            return tests_list
        except Exception as error:
            logging.error(f"Error in get_all_tests_controller function: {error}")

    def delete_test_controller(self, test_id):
        """[Controller to delete a user]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [deleted user details]
        """
        try:
            logging.info("executing delete_test_controller function")
            response = self.CRUDListOfMedicalTests.delete(medical_test_id=test_id)
            response.update({"status": "Medical Test Deleted Successfully"})
            return response
        except Exception as error:
            logging.error(f"Error in delete_test_controller function: {error}")
            raise {"error": "Invalid username or password"}


class ListOfMedicinesController:
    def __init__(self):
        self.CRUDListOfMedicines = CRUDListOfMedicines()

    def add_medicine_controller(self, name, company):
        """[Controller to register new user]

        Args:
            request ([dict]): [create new user request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing add new medicine function")
            name_upper = name.upper()
            company_upper = company.upper()
            medicine_obj = self.CRUDListOfMedicines.read(medicine=name_upper)
            if medicine_obj:
                medicine_obj.update({"status": "Medicine already exist"})
                return medicine_obj
            medicine_id = self.CRUDListOfMedicines.create(
                **{"name": name_upper, "company": company_upper}
            )
            return {
                "medicine_id": medicine_id,
                "medicine_name": name_upper,
                "company": company_upper,
                "status": "Medicine added successfully",
            }
        except Exception as error:
            logging.error(f"Error in create_medicine_controller function: {error}")
            raise error

    def get_all_medicines_controller(self):
        """[Controller to get all users]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [list]: [list of all the users in the system]
        """
        try:
            logging.info("executing get_all_tests_controller function")
            tests_list = self.CRUDListOfMedicines.read_all()
            return tests_list
        except Exception as error:
            logging.error(f"Error in get_all_tests_controller function: {error}")

    def delete_medicine_controller(self, medicine_id):
        """[Controller to delete a user]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [deleted user details]
        """
        try:
            logging.info("executing delete_medicine_controller function")
            response = self.CRUDListOfMedicines.delete(medicine_id=medicine_id)
            response.update({"status": "Medicine Deleted Successfully"})
            return response
        except Exception as error:
            logging.error(f"Error in delete_medicine_controller function: {error}")
            raise {"error": "Invalid username or password"}


class ListOfPrecautionsController:
    def __init__(self):
        self.CRUDListOfPrecautions = CRUDListOfPrecautions()

    def add_instruction_controller(self, instruction):
        """[Controller to register new user]

        Args:
            request ([dict]): [create new user request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing add new instruction function")
            instruction_upper = instruction.upper()
            instruction_obj = self.CRUDListOfPrecautions.read(
                instruction_name=instruction_upper
            )
            if instruction_obj:
                instruction_obj.update({"status": "Instruction already exist"})
                return instruction_obj
            instruction_id = self.CRUDListOfPrecautions.create(
                **{"instructions": instruction_upper}
            )
            return {
                "instruction_id": instruction_id,
                "instruction_name": instruction_upper,
                "status": "Instruction added successfully",
            }
        except Exception as error:
            logging.error(f"Error in create_instruction_controller function: {error}")
            raise error

    def get_all_instructions_controller(self):
        """[Controller to get all users]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [list]: [list of all the users in the system]
        """
        try:
            logging.info("executing get_all_instructions_controller function")
            instructions_list = self.CRUDListOfPrecautions.read_all()
            return instructions_list
        except Exception as error:
            logging.error(f"Error in get_all_instructions_controller function: {error}")

    def delete_instruction_controller(self, instruction_id):
        """[Controller to delete a user]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [deleted user details]
        """
        try:
            logging.info("executing delete_instruction_controller function")
            response = self.CRUDListOfPrecautions.delete(instruction_id=instruction_id)
            response.update({"status": "Instruction Deleted Successfully"})
            return response
        except Exception as error:
            logging.error(f"Error in delete_instruction_controller function: {error}")
            raise {"error": "Invalid username or password"}


class Common:
    def __init__(self):
        self.abha_url = os.environ["abha_url"]
        self.s3_location = os.environ["s3_location"]
        self.gateway_url = os.environ["gateway_url"]
        self.CRUD_docDetails = CRUDDocDetails()

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
