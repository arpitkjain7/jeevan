from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.hid_request import AbhaRegistration
from core.controllers.hid_controller import HIDController
from core import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
hid_router = APIRouter()


@hid_router.post("/v1/HID/aadhaar/generateOTP")
def create_health_id(aadhaar_number: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/aadhaar/generateOTP endpoint")
        logging.debug(f"Request: {aadhaar_number=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().aadhaar_generateOTP(aadhaar_number=aadhaar_number)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/HID/aadhaar/generateOTP endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HID/aadhaar/generateOTP endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hid_router.post("/v1/HID/aadhaar/verifyOTP")
def create_health_id(otp: str, txn_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/aadhaar/verifyOTP endpoint")
        logging.debug(f"Request: {otp=}")
        logging.debug(f"Request: {txn_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().aadhaar_verifyOTP(otp=otp, txn_id=txn_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/HID/aadhaar/verifyOTP endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HID/aadhaar/verifyOTP endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hid_router.post("/v1/HID/aadhaar/generateMobileOTP")
def create_health_id(
    mobile_number: str, txn_id: str, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info(f"Calling /v1/HID/aadhaar/generateMobileOTP endpoint")
        logging.debug(f"Request: {mobile_number=}")
        logging.debug(f"Request: {txn_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().aadhaar_generateMobileOTP(
                mobile_number=mobile_number, txn_id=txn_id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/HID/aadhaar/generateMobileOTP endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HID/aadhaar/generateMobileOTP endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hid_router.post("/v1/HID/aadhaar/verifyMobileOTP")
def create_health_id(otp: str, txn_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/aadhaar/verifyMobileOTP endpoint")
        logging.debug(f"Request: {otp=}")
        logging.debug(f"Request: {txn_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().aadhaar_verifyMobileOTP(otp=otp, txn_id=txn_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/HID/aadhaar/verifyMobileOTP endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HID/aadhaar/verifyMobileOTP endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hid_router.post("/v1/HID/aadhaar/abhaRegistration")
def create_health_id(
    reg_request: AbhaRegistration, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info(f"Calling /v1/HID/aadhaar/abhaRegistration endpoint")
        logging.debug(f"Request: {reg_request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().aadhaar_registration(reg_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/HID/aadhaar/abhaRegistration endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HID/aadhaar/abhaRegistration endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
