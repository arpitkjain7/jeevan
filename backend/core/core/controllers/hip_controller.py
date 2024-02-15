from core.crud.hims_hip_crud import CRUDHIP
from core.crud.hims_users_crud import CRUDUser
from core.utils.custom.qrcode_generation import qrcode_generator
from core import logger
import os

logging = logger(__name__)


class HIPController:
    def __init__(self):
        self.CRUDHIP = CRUDHIP()
        self.CRUDUser = CRUDUser()
        self.hip_base_url = os.environ["hip_base_url"]

    def create_hip(self, request):
        """[Controller to create new hip record]

        Args:
            request ([dict]): [create new hip request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing create new hip function")
            request_dict = request.dict()
            logging.info("Creating HIP record")
            record_id = self.CRUDHIP.create(**request_dict)
            return {"id": record_id, "hip_id": request_dict.get("hip_id")}
        except Exception as error:
            logging.error(f"Error in HIPController.create_hip function: {error}")
            raise error

    def get_hip(self, hip_id: str):
        """[Controller to get HIP record]

        Args:
            hip_id ([str]): [hip_id for getting HIP records]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing get pmr function")
            logging.info(f"Getting the PMR record for {hip_id=}")
            return self.CRUDHIP.read(hip_ip=hip_id)
        except Exception as error:
            logging.error(f"Error in HIPController.get_hip function: {error}")
            raise error

    def get_QR_hip(self, hip_id: str, department_id: str):
        try:
            logging.info("executing get_QR_hip function")
            logging.info(f"Getting the QR for {hip_id=}")
            if department_id:
                hip_url = (
                    f"{self.hip_base_url}?hip-id={hip_id}&counter-id={department_id}"
                )
            else:
                hip_url = f"{self.hip_base_url}?hip-id={hip_id}"
            return qrcode_generator(url=hip_url)
        except Exception as error:
            logging.error(f"Error in HIPController.get_QR_hip function: {error}")
            raise error

    def get_all_hip(self):
        """[Controller to get all HIP records]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing get all HIP function")
            logging.info(f"Getting the HIP records")
            return self.CRUDHIP.read_all()
        except Exception as error:
            logging.error(f"Error in HIPController.get_all_hip function: {error}")
            raise error

    def get_hip_for_user(self, username: str):
        try:
            logging.info("executing get_hip_for_user function")
            logging.info(f"Getting HIPs for the user")
            user_obj = self.CRUDUser.read_by_username(username=username)
            user_hip_obj = user_obj.get("hip_details")
            hip_list = []
            if user_hip_obj:
                for hip_id in user_hip_obj.keys():
                    hip_list.append(self.CRUDHIP.read(hip_ip=hip_id))
            return hip_list
        except Exception as error:
            logging.error(f"Error in HIPController.get_hip_for_user function: {error}")
            raise error
