from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.patient_request import FetchRegisterationMode
from core.controllers.pmr_controller import PMRController
from core import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
patient_router = APIRouter()


@patient_router.post("/v1/patient/fetchModes")
def fetch_auth_modes(
    fetch_request: FetchRegisterationMode, token: str = Depends(oauth2_scheme)
):
    pass
    # try:
    #     logging.info("Calling /v1/patient/fetchModes endpoint")
    #     logging.debug(f"Request: {fetch_request}")
    #     authenticated_user_details = decodeJWT(token=token)
    #     if authenticated_user_details:
    #         return PMRController().create_pmr(request=pmr_request)
    #     else:
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail="Invalid access token",
    #             headers={"WWW-Authenticate": "Bearer"},
    #         )
    # except HTTPException as httperror:
    #     logging.error(f"Error in /v1/patient/fetchModes endpoint: {httperror}")
    #     raise httperror
    # except Exception as error:
    #     logging.error(f"Error in /v1/patient/fetchModes endpoint: {error}")
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=str(error),
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
