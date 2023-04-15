from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.hid_request import (
    AbhaRegistration,
    OTPVerification,
    MobileOTP,
    AadhaarNumber,
    HealthNumber,
)
from core.controllers.hid_controller import HIDController
from core import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
hid_router = APIRouter()


@hid_router.post("/v1/HID/registration/aadhaar/generateOTP")
def create_health_id(request: AadhaarNumber, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/aadhaar/generateOTP endpoint")
        logging.debug(f"Request: {request.aadhaar_number=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().aadhaar_generateOTP(
                aadhaar_number=request.aadhaar_number
            )
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


@hid_router.post("/v1/HID/registration/aadhaar/verifyOTP")
def create_health_id(request: OTPVerification, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/aadhaar/verifyOTP endpoint")
        logging.debug(f"Request: {request.otp=}")
        logging.debug(f"Request: {request.txn_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().aadhaar_verifyOTP(
                otp=request.otp, txn_id=request.txn_id
            )
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


@hid_router.post("/v1/HID/registration/aadhaar/generateMobileOTP")
def create_health_id(request: MobileOTP, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/aadhaar/generateMobileOTP endpoint")
        logging.debug(f"Request: {request.mobile_number=}")
        logging.debug(f"Request: {request.txn_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().aadhaar_generateMobileOTP(
                mobile_number=request.mobile_number, txn_id=request.txn_id
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


@hid_router.post("/v1/HID/registration/aadhaar/verifyMobileOTP")
def create_health_id(request: OTPVerification, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/aadhaar/verifyMobileOTP endpoint")
        logging.debug(f"Request: {request.otp=}")
        logging.debug(f"Request: {request.txn_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().aadhaar_verifyMobileOTP(
                otp=request.otp, txn_id=request.txn_id
            )
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


@hid_router.post("/v1/HID/registration/aadhaar/abhaRegistration")
def create_health_id(request: AbhaRegistration, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/aadhaar/abhaRegistration endpoint")
        logging.debug(f"Request: {request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().aadhaar_registration(request)
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


@hid_router.get("/v1/HID/registration/aadhaar/checkAbhaAvailability")
def check_available_health_id(
    request: HealthNumber, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info(
            f"Calling /v1/HID/aadhaar/registration/checkAbhaAvailability endpoint"
        )
        logging.debug(f"Request: {request.health_number=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().abha_verification(health_id=request.health_number)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/HID/aadhaar/registration/checkAbhaAvailability endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HID/aadhaar/abhaRegistration endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hid_router.post("/v1/HID/forgot/aadhaar/generateOtp")
def generate_aadhaar_otp(request: AadhaarNumber, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/forgot/aadhaar/generateOtp endpoint")
        logging.debug(f"Request: {request.aadhaar_number=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().forgot_generateOtp(
                aadhaar_number=request.aadhaar_number
            )
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


@hid_router.post("/v1/HID/forgot/aadhaar/verifyOtp")
def verify_aadhaar_otp(request: OTPVerification, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/forgot/aadhaar/generateOtp endpoint")
        logging.debug(f"Request: {request.otp=}")
        logging.debug(f"Request: {request.txn_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().forgot_verifyOtp(
                otp=request.otp, txn_id=request.txn_id
            )
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
