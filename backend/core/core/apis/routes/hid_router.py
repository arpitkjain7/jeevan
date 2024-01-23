from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.hid_request import (
    AbhaRegistration,
    OTPVerification,
    MobileNumber,
    AadhaarNumber,
    HealthNumber,
    AbhaRegistration_MobileOTP,
    MobileOTP,
    PatientData,
    MobileNumber,
    AbhaAuth,
    AbhaAuthConfirm,
)
from core.controllers.hid_controller import HIDController
from core import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
hid_router = APIRouter()


@hid_router.post("/v1/HID/registration/aadhaar/generateOTP")
def aadhaar_generateOTP(request: AadhaarNumber, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/aadhaar/generateOTP endpoint")
        logging.debug(f"Request: {request.aadhaarNumber=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().aadhaar_generateOTP(
                aadhaar_number=request.aadhaarNumber
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
def aadhaar_verifyOTP(request: OTPVerification, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/aadhaar/verifyOTP endpoint")
        logging.debug(f"Request: {request.otp=}")
        logging.debug(f"Request: {request.txnId=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().aadhaar_verifyOTP(
                otp=request.otp, txn_id=request.txnId
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
def aadhaar_generateMobileOTP(request: MobileOTP, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/aadhaar/generateMobileOTP endpoint")
        logging.debug(f"Request: {request.mobileNumber=}")
        logging.debug(f"Request: {request.txnId=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().aadhaar_generateMobileOTP(
                mobile_number=request.mobileNumber, txn_id=request.txnId
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
def aadhaar_verifyMobileOTP(
    request: OTPVerification, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info(f"Calling /v1/HID/aadhaar/verifyMobileOTP endpoint")
        logging.debug(f"Request: {request.otp=}")
        logging.debug(f"Request: {request.txnId=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().aadhaar_verifyMobileOTP(
                otp=request.otp, txn_id=request.txnId
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
def aadhaar_abhaRegistration(
    request: AbhaRegistration, token: str = Depends(oauth2_scheme)
):
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


@hid_router.post("/v1/HID/forgot/aadhaar/generateOtp")
def generate_aadhaar_otp(request: AadhaarNumber, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/forgot/aadhaar/generateOtp endpoint")
        logging.debug(f"Request: {request.aadhaarNumber=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().forgot_generateOtp(
                aadhaar_number=request.aadhaarNumber
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
        logging.debug(f"Request: {request.txnId=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().forgot_verifyOtp(
                otp=request.otp, txn_id=request.txnId
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


@hid_router.post("/v1/registration/mobile/generateOtp")
def mobile_generateOTP(request: MobileNumber, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/registration/mobile/generateOtp endpoint")
        logging.debug(f"Request: {request.mobileNumber=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().generateMobileOTP(mobile_number=request.mobileNumber)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/registration/mobile/generateOtp endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/registration/mobile/generateOtp endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hid_router.post("/v1/registration/mobile/verifyOtp")
def mobile_verifyOTP(request: OTPVerification, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/registration/mobile/verifyOtp")
        logging.debug(f"Request: {request.otp=}")
        logging.debug(f"Request: {request.txnId=}")
        logging.debug(f"Token: {token=}")
        authenticated_user_details = decodeJWT(token=token)
        logging.debug(f"UserDetails: {authenticated_user_details=}")
        if authenticated_user_details:
            return HIDController().verifyMobileOTP(
                otp=request.otp, txn_id=request.txnId
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/registration/mobile/verifyOtp: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/registration/mobile/verifyOtp: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hid_router.post("/v1/registration/mobile/createHealthId")
def mobile_abhaRegistration(
    request: AbhaRegistration_MobileOTP, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info(f"Calling /v1/registration/mobile/createHealthId endpoint")
        logging.debug(f"Request: {request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().mobile_abha_registration(request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/registration/mobile/createHealthId endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(
            f"Error in /v1/registration/mobile/createHealthId endpoint: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hid_router.post("/v1/profile/getAbhaCard")
def profile_getAbhaCard(request: PatientData, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/profile/getAbhaCard endpoint")
        logging.debug(f"Request: {request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().get_abha_card(patient_id=request.patientId)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/profile/getAbhaCard endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/profile/getAbhaCard endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hid_router.post("/v1/profile/getAbhaCardBytes")
def profile_getAbhaCardBytes(request: PatientData, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/profile/getAbhaCardBytes endpoint")
        logging.debug(f"Request: {request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().get_abha_card_bytes(patient_id=request.patientId)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/profile/getAbhaCardBytes endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/profile/getAbhaCardBytes endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hid_router.post("/v1/HID/searchAbha")
def search_abha(request: HealthNumber, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/searchAbha endpoint")
        logging.debug(f"Request: {request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().search_abha(abha_number=request.healthNumber)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/HID/searchAbha endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HID/searchAbha endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hid_router.post("/v1/HID/searchMobile")
def search_mobile(request: MobileNumber, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/searchMobile endpoint")
        logging.debug(f"Request: {request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().search_mobile(mobile_number=request.mobileNumber)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/HID/searchMobile endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HID/searchMobile endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hid_router.post("/v1/HID/verifyMobileOtp")
def verify_mobile_otp(request: OTPVerification, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/verifyMobileOtp endpoint")
        logging.debug(f"Request: {request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().verify_login_otp(request=request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/HID/verifyMobileOtp endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HID/verifyMobileOtp endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hid_router.post("/v1/HID/authInit")
def abha_auth_init(request: AbhaAuth, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/authInit endpoint")
        logging.debug(f"Request: {request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().abha_auth_init(request=request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/HID/authInit endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HID/authInit endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hid_router.post("/v1/HID/authConfirm")
def abha_auth_confirm(request: AbhaAuthConfirm, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/HID/authConfirm endpoint")
        logging.debug(f"Request: {request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().abha_auth_confirm(request=request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/HID/authConfirm endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HID/authConfirm endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hid_router.post("/v3/HID/registration/aadhaar/generateOTP")
def aadhaar_generateOTP_v3(request: AadhaarNumber, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v3/HID/registration/aadhaar/generateOTP endpoint")
        logging.debug(f"Request: {request.aadhaarNumber=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIDController().aadhaar_generateOTP_v3(
                aadhaar_number=request.aadhaarNumber
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v3/HID/registration/aadhaar/generateOTP endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(
            f"Error in /v3/HID/registration/aadhaar/generateOTP endpoint: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
