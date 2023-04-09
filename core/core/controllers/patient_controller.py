from core.crud.hims_patientDetails_crud import CRUDPatientDetails
from core.commons.external_call import APIInterface
from core.utils.custom.session_helper import get_session_token
from core import logger
from datetime import datetime
import os
import uuid

logging = logger(__name__)


class PatientController:
    def __init__(self):
        self.CRUDPatientDetails = CRUDPatientDetails()

    def fetch_auth_modes(self, request):
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
            request_dict = request.dict()
            logging.info("Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            fetch_modes_url = f"{self.gateway_url}/v0.5/users/auth/fetch-modes"
            request_id = uuid.uuid1()
            resp_code, resp_json = APIInterface().post(
                route=fetch_modes_url,
                data={
                    "requestId": request_id,
                    "timestamp": datetime.now().timestamp(),
                    "query": {
                        "id": request_dict.get("abha_number"),
                        "purpose": request_dict.get("purpose"),
                        "requester": {"type": "HIP", "id": request_dict.get("hip_id")},
                    },
                },
                headers={
                    "X-CM-ID": "sbx",
                    "Authorization": f"Bearer {gateway_access_token}",
                },
            )
            if resp_code == "202":
                pass
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
