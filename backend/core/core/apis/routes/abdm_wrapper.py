from fastapi import APIRouter, HTTPException, status, Depends, UploadFile
from typing import List
from collections import defaultdict
from datetime import date
from core import logger
from commons.auth import decodeJWT

logging = logger(__name__)
abdm_router = APIRouter()


@abdm_router.get("/v1/patients/{patientId}")
def getPatient(patientId: str):
    try:
        logging.info(f"Calling /v1/patients/{patientId} endpoint")
        logging.debug(f"Request: {patientId}")
    except HTTPException as httperror:
        logging.error(f"Error in /v1/patients/{patientId} endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/patients/{patientId} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
