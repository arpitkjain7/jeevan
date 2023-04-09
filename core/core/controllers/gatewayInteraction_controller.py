from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteration
from core import logger

logging = logger(__name__)


class GatewayController:
    def __init__(self):
        self.CRUDGatewayInteration = CRUDGatewayInteration()

    def get_status(self, request_id: str):
        """[Controller to fetch patient auth modes]

        Args:
            request ([dict]): [fetch auth modes request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing  fetch_auth_modes function")
            logging.info("Getting session access Token")
            return self.CRUDGatewayInteration.read(request_id=request_id)
        except Exception as error:
            logging.error(f"Error in HIPController.create_hip function: {error}")
            raise error
