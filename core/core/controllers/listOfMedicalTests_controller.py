from core.crud.hims_listOfMedicalTests_crud import CRUDListOfMedicalTests
from commons.auth import encrypt_password, verify_hash_password, signJWT
from core import logger

logging = logger(__name__)


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


'''def update_comlaint_controller(self, request):
        """[Controller for user login]

        Args:
            request ([dict]): [user login details]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing update complaint function")
            complaint_obj = self.CRUDListOfComplaints.read(complaint=request.complaint)
            if complaint_obj:
                complaint_obj.update(
                        {"complaint": request.complaint,}
                    )
                return {
                    "complaint_id": complaint_obj.id,
                    "complaint_name": request.get("complaint"),
                    "status": "Complaint updated successfully",
                }
            else:
                return None
        except Exception as error:
            logging.error(f"Error in update_complaint_controller function: {error}")
            raise error'''
