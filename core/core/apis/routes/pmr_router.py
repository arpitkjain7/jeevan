from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.pmr_request import PMR
from core.controllers.pmr_controller import PMRController
from core import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
pmr_router = APIRouter()


@pmr_router.post("/v1/pmr/create")
def create_pmr(pmr_request: PMR, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/pmr/create endpoint")
        logging.debug(f"Request: {pmr_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().create_pmr_controller(request=pmr_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/create endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/create endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
