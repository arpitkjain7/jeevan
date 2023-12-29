from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from core.utils.custom.encryption_helper import encrypt_data
from core.controllers.dataTransfer_controller import DataTransferController

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
dataTransfer_router = APIRouter()


@dataTransfer_router.post("/v0.5/health-information/hip/request")
def hi_data_request(consent_notify_request: dict):
    try:
        print("Calling /v0.5/health-information/hip/request endpoint")
        print(f"Request: {consent_notify_request}")
        response = DataTransferController().data_request(request=consent_notify_request)
        return response
    except Exception as error:
        print(f"Error in /v0.5/health-information/hip/request endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@dataTransfer_router.post("/test")
def encrypt_data_endpoint(consent_notify_request: dict):
    try:
        print("Calling /v0.5/consents/hip/notify endpoint")
        print(f"Request: {consent_notify_request}")
        return encrypt_data(
            stringToEncrypt=consent_notify_request.get("data"),
            requesterKeyMaterial=consent_notify_request.get("key_details"),
        )
    except Exception as error:
        print(f"Error in /v0.5/consents/hip/notify endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
