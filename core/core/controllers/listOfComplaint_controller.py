from core.crud.hims_listOfComplaints_crud import CRUDListOfComplaints
from commons.auth import encrypt_password, verify_hash_password, signJWT
from core import logger

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
            complaint_id = self.CRUDListOfComplaints.create(**{"complaint": complaint_lower})
            return {
                "complaint_id": complaint_id,
                "complaint": complaint_lower,
                "status": "Complaint added successfully"
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


    def delete_complaint_controller(self,complaint_id):
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