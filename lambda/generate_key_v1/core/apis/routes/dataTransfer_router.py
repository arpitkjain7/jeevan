from fastapi import APIRouter, HTTPException, status
from core.controllers.dataTransfer_controller import DataTransferController

dataTransfer_router = APIRouter()


@dataTransfer_router.get("/v1/cliniq360/generateKey")
def generate_key():
    try:
        print("Calling /v1/cliniq360/generateKey endpoint")
        return DataTransferController().generate_key()
    except Exception as error:
        print(f"Error in /v1/cliniq360/generateKey endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
