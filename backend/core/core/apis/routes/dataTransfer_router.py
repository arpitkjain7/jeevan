from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core import logger
from core.controllers.dataTransfer_controller import DataTransferController

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
dataTransfer_router = APIRouter()


@dataTransfer_router.post("/v0.5/consents/hip/notify")
def hip_notify(consent_notify_request: dict):
    try:
        logging.info("Calling /v0.5/consents/hip/notify endpoint")
        logging.debug(f"Request: {consent_notify_request}")
        return DataTransferController().hip_notify(request=consent_notify_request)
    except Exception as error:
        logging.error(f"Error in /v0.5/consents/hip/notify endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@dataTransfer_router.post("/v0.5/health-information/hip/request")
def hi_data_request(consent_notify_request: dict):
    try:
        logging.info("Calling /v0.5/health-information/hip/request endpoint")
        logging.debug(f"Request: {consent_notify_request}")
        return DataTransferController().data_request(request=consent_notify_request)
    except Exception as error:
        logging.error(
            f"Error in /v0.5/health-information/hip/request endpoint: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@dataTransfer_router.post("/v1/data_transfer_ack")
def data_transfer_ack(data_transfer_ack_request: dict):
    try:
        logging.info("Calling /v1/data_transfer_ack endpoint")
        logging.debug(f"Request: {data_transfer_ack}")
        return DataTransferController().send_data_transfer_ack(
            request=data_transfer_ack_request
        )
    except Exception as error:
        logging.error(f"Error in /v1/data_transfer_ack endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
