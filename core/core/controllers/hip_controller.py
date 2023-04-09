from core.crud.hims_hip_crud import CRUDHIP
from core import logger

logging = logger(__name__)


class HIPController:
    def __init__(self):
        self.CRUDHIP = CRUDHIP()

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
            hip_id = self.CRUDHIP.create(**request_dict)
            return {"hip_id": hip_id}
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
