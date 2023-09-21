from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.hip_request import CreateHIP
from core.controllers.hip_controller import HIPController
from core import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
hip_router = APIRouter()


@hip_router.post("/v1/HIP/create")
def create_hip(hip_request: CreateHIP, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/HIP/create endpoint")
        logging.debug(f"Request: {hip_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIPController().create_hip(request=hip_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/HIP/create endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HIP/create endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hip_router.get("/v1/HIP/listAll")
def get_all_HIPs(token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HIP/listAll endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIPController().get_all_hip()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/HIP/listAll endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HIP/listAll endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hip_router.get("/v1/HIP/{hip_id}")
def get_hip(hip_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HIP/{hip_id} endpoint")
        logging.debug(f"Request: {hip_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIPController().get_hip(hip_id=hip_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/HIP/{hip_id} endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HIP/{hip_id} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hip_router.get("/v1/HIP/getQR/{hip_id}")
def get_QR_hip(
    hip_id: str, department_id: str = None, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info(f"Calling /v1/HIP/getQR/{hip_id} endpoint")
        logging.debug(f"Request: {hip_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIPController().get_QR_hip(
                hip_id=hip_id, department_id=department_id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/HIP/getQR/{hip_id} endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HIP/getQR/{hip_id} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
