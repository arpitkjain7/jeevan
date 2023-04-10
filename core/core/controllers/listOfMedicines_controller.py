from core.crud.hims_listOfMedicines_crud import CRUDListOfMedicines
from commons.auth import encrypt_password, verify_hash_password, signJWT
from core import logger

logging = logger(__name__)


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
            medicine_obj = self.CRUDListOfMedicines.read(name=name_upper)
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
