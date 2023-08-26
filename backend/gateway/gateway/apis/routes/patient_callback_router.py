from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from gateway.controllers.patient_callback_controller import PatientCallbackController
from gateway import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
patient_callback_router = APIRouter()


@patient_callback_router.post("/v1.0/patients/profile/share")
def patient_profileShare(request: Request):
    try:
        logging.info("Calling /v1.0/patients/profile/share endpoint")
        hip_id = request.headers.get("X-HIP-ID")
        logging.debug(f"Request: {request.dict()}")
        return PatientCallbackController().patient_share(
            request=request.dict(), hip_id=hip_id
        )
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


@patient_callback_router.post("/v0.5/care-contexts/discover")
async def discover_patient(request: Request):
    try:
        logging.info("Calling /v0.5/care-contexts/discover endpoint")
        hip_id = request.headers.get("X-HIP-ID")
        logging.debug(f"hip_id: {hip_id}")
        request_json = await request.json()
        logging.debug(f"Request: {request_json}")
        return PatientCallbackController().discover_patient(
            request=request_json, hip_id=hip_id
        )
    except HTTPException as httperror:
        logging.error(f"Error in /v0.5/care-contexts/discover endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v0.5/care-contexts/discover endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@patient_callback_router.post("/v0.5/links/link/init")
async def link_patient(request: Request):
    try:
        logging.info("Calling /v0.5/links/link/init endpoint")
        hip_id = request.headers.get("X-HIP-ID")
        logging.debug(f"hip_id: {hip_id}")
        request_json = await request.json()
        logging.debug(f"Request: {request_json}")
        return PatientCallbackController().link_patient(
            request=request_json, hip_id=hip_id
        )
    except HTTPException as httperror:
        logging.error(f"Error in /v0.5/links/link/init endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v0.5/links/link/init endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@patient_callback_router.post("/v0.5/links/link/confirm")
async def link_on_confirm(request: Request):
    try:
        logging.info("Calling /v0.5/links/link/confirm endpoint")
        hip_id = request.headers.get("X-HIP-ID")
        logging.debug(f"hip_id: {hip_id}")
        request_json = await request.json()
        logging.debug(f"Request: {request_json}")
        return PatientCallbackController().link_confirm(
            request=request_json, hip_id=hip_id
        )
    except HTTPException as httperror:
        logging.error(f"Error in /v0.5/links/link/confirm endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v0.5/links/link/confirm endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@patient_callback_router.post("/v0.5/patients/sms/on-notify")
def patient_sms_on_notify(sms_on_notify_request: dict):
    try:
        logging.info("Calling /v0.5/patients/sms/on-notify endpoint")
        logging.debug(f"Request: {sms_on_notify_request}")
        return PatientCallbackController().deep_link_ack(request=sms_on_notify_request)
    except HTTPException as httperror:
        logging.error(f"Error in /v0.5/patients/sms/on-notify endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v0.5/patients/sms/on-notify endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
