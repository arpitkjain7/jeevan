from core.crud.hims_listOfDiagnosis_crud import CRUDListOfDiagosis
from commons.auth import encrypt_password, verify_hash_password, signJWT
from core import logger

logging = logger(__name__)


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
