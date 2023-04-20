from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.patient_request import (
    FetchRegisterationMode,
    AuthInit,
    VerifyOtp,
)
from core.controllers.patient_controller import PatientController
from core import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
patient_router = APIRouter()


@patient_router.post("/v1/patient/fetchModes")
def fetch_auth_modes(
    request: FetchRegisterationMode, token: str = Depends(oauth2_scheme)
):
    pass
    try:
        logging.info("Calling /v1/patient/fetchModes endpoint")
        logging.debug(f"Request: {request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            hip_id = authenticated_user_details.get("hip_id")
            return PatientController().fetch_auth_modes(request=request, hip_id=hip_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/patient/fetchModes endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/patient/fetchModes endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@patient_router.post("/v1/patient/auth/init")
def auth_init(request: AuthInit, token: str = Depends(oauth2_scheme)):
    pass
    try:
        logging.info("Calling /v1/patient/auth/init endpoint")
        logging.debug(f"Request: {request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            hip_id = authenticated_user_details.get("hip_id")
            return PatientController().auth_init(request=request, hip_id=hip_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/patient/auth/init endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/patient/auth/init endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@patient_router.post("/v1/patient/auth/verifyOtp")
def auth_verifyOtp(request: VerifyOtp, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/patient/auth/verifyOtp endpoint")
        logging.debug(f"Request: {request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PatientController().verify_otp(request=request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/patient/auth/verifyOtp endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/patient/auth/verifyOtp endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@patient_router.post("/v1.0/patients/profile/share")
def patient_profileShare(request: dict):
    try:
        logging.info("Calling /v1.0/patients/profile/share endpoint")
        logging.debug(f"Request: {request}")
        return PatientController().patient_share(request=request)
    except HTTPException as httperror:
        logging.error(f"Error in /v1.0/patients/profile/share endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1.0/patients/profile/share endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
