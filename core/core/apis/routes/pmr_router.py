from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.pmr_request import PMR
from core.controllers.pmr_controller import PMRController
from core import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
pmr_router = APIRouter()


@pmr_router.post("/v1/PMR/create")
def create_pmr(pmr_request: PMR, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/pmr/create endpoint")
        logging.debug(f"Request: {pmr_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            hip_id = authenticated_user_details.get("hip_id")
            return PMRController().create_pmr(request=pmr_request, hip_id=hip_id)
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


@pmr_router.post("/v1/PMR/sync/{pmr_id}")
def sync_pmr_to_gateway(pmr_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/pmr/sync endpoint")
        logging.debug(f"Request: {pmr_id}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            hip_id = authenticated_user_details.get("hip_id")
            return PMRController().sync_pmr(pmr_id=pmr_id, hip_id=hip_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/sync endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/sync endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.get("/v1/PMR/list/{patient_id}")
def get_pmr_by_patientId(patient_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/PMR/list/{patient_id} endpoint")
        logging.debug(f"Request: {patient_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().get_pmr_with_patientId(patient_id=patient_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/list endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/list endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.get("/v1/PMR/{pmr_id}")
def get_pmr(pmr_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/pmr/{pmr_id} endpoint")
        logging.debug(f"Request: {pmr_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().get_pmr(pmr_id=pmr_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/get endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/get endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
