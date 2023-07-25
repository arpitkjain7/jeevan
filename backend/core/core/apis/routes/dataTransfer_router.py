from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi import BackgroundTasks
from core import logger
from commons.auth import decodeJWT
from core.utils.custom.encryption_helper import encrypt_data
from core.controllers.dataTransfer_controller import DataTransferController
from core.controllers.dataTransfer_controller import data_request

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
dataTransfer_router = APIRouter()


@dataTransfer_router.post("/v0.5/consents/hip/notify")
def consent_notify(consent_notify_request: dict):
    try:
        logging.info("Calling /v0.5/consents/hip/notify endpoint")
        logging.debug(f"Request: {consent_notify_request}")
        return DataTransferController().consent_notify(request=consent_notify_request)
    except Exception as error:
        logging.error(f"Error in /v0.5/consents/hip/notify endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@dataTransfer_router.post("/v0.5/health-information/hip/request")
def hi_data_request(consent_notify_request: dict, background_tasks: BackgroundTasks):
    try:
        logging.info("Calling /v0.5/health-information/hip/request endpoint")
        logging.debug(f"Request: {consent_notify_request}")
        background_tasks.add_task(data_request, consent_notify_request)
        return {"status": "success"}
        # response = DataTransferController().data_request(request=consent_notify_request)
        # return response
    except Exception as error:
        logging.error(
            f"Error in /v0.5/health-information/hip/request endpoint: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@dataTransfer_router.post("/test")
def encrypt_data_endpoint(consent_notify_request: dict):
    try:
        logging.info("Calling /v0.5/consents/hip/notify endpoint")
        logging.debug(f"Request: {consent_notify_request}")
        return encrypt_data(
            stringToEncrypt=consent_notify_request.get("data"),
            requesterKeyMaterial=consent_notify_request.get("key_details"),
        )
    except Exception as error:
        logging.error(f"Error in /v0.5/consents/hip/notify endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
