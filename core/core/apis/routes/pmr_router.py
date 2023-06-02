from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.pmr_request import (
    PMR,
    CreateComplaint,
    CreateDiagnosis,
    CreateMedicalTest,
    CreateMedication,
)
from core.controllers.pmr_controller import PMRController
from core import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
pmr_router = APIRouter()


@pmr_router.post("/v1/PMR/recordVitals")
def recordVitals(pmr_request: PMR, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/pmr/recordVitals endpoint")
        logging.debug(f"Request: {pmr_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            hip_id = authenticated_user_details.get("hip_id")
            return PMRController().create_pmr(request=pmr_request, hip_id=hip_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/recordVitals endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/recordVitals endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/recordDiagnosis")
def recordDiagnosis(
    diagnosis_request: CreateDiagnosis, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/recordDiagnosis endpoint")
        logging.debug(f"Request: {diagnosis_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().create_diagnosis(request=diagnosis_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/recordDiagnosis endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/recordDiagnosis endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/recordComplaints")
def recordComplaints(
    complaint_request: CreateComplaint, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/recordComplaints endpoint")
        logging.debug(f"Request: {complaint_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().create_complaints(request=complaint_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/recordComplaints endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/recordComplaints endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/recordMedication")
def recordMedication(
    medication_request: CreateMedication, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/recordMedication endpoint")
        logging.debug(f"Request: {medication_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().create_medication(request=medication_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/recordMedication endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/recordMedication endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/recordMedicalTest")
def recordMedicalTest(
    medicalTest_request: CreateMedicalTest, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/recordMedicalTest endpoint")
        logging.debug(f"Request: {medicalTest_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().create_medicalTest(request=medicalTest_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/recordMedicalTest endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/recordMedicalTest endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/sync/{pmr_id}")
def sync_pmr_to_gateway(pmr_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/pmr/sync endpoint")
        logging.debug(f"Request: {pmr_id}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            hip_id = authenticated_user_details.get("hip_id")
            return PMRController().sync_pmr(pmr_id=pmr_id, hip_id=hip_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/sync endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/sync endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.get("/v1/PMR/list/{patient_id}")
def get_pmr_by_patientId(patient_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/PMR/list/{patient_id} endpoint")
        logging.debug(f"Request: {patient_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().get_pmr_with_patientId(patient_id=patient_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/list endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/list endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.get("/v1/PMR/{pmr_id}")
def get_pmr(pmr_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/pmr/{pmr_id} endpoint")
        logging.debug(f"Request: {pmr_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().get_pmr(pmr_id=pmr_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/get endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/get endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.delete("/v1/PMR/{pmr_id}")
def delete_pmr(pmr_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/pmr/{pmr_id} endpoint")
        logging.debug(f"Request: {pmr_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().delete_pmr(pmr_id=pmr_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/get endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/get endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
