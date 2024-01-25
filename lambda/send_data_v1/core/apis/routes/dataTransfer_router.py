from fastapi import APIRouter, HTTPException, status
from core.controllers.dataTransfer_controller import DataTransferController

dataTransfer_router = APIRouter()


@dataTransfer_router.post("/v1/cliniq360/sendData")
def send_data(bucket_name: str, object_key: str):
    try:
        print("Calling /v1/cliniq360/encrypt endpoint")
        print(f"Request: {bucket_name=} {object_key=}")
        DataTransferController().send_data(
            bucket_name=bucket_name, object_key=object_key
        )
    except Exception as error:
        print(f"Error in /v1/cliniq360/encrypt endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@dataTransfer_router.post("/v1/cliniq360/decryptReceivedData")
def decrypt_received_data(bucket_name: str, object_key: str):
    try:
        print("Calling /v1/cliniq360/decrypt endpoint")
        print(f"Request: {bucket_name=} {object_key=}")
        pass
    except Exception as error:
        print(f"Error in /v1/cliniq360/decrypt endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@dataTransfer_router.get("/v1/cliniq360/generateKey")
def generate_key():
    try:
        print("Calling /v1/cliniq360/generateKey endpoint")
        return DataTransferController().generate()
    except Exception as error:
        print(f"Error in /v1/cliniq360/generateKey endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
