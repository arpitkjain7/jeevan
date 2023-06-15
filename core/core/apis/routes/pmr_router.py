from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.pmr_request import (
    PMR,
    CreateVital,
    CreateComplaint,
    CreateDiagnosis,
    CreateCondition,
    CreateMedicalTest,
    CreateMedication,
    CreateMedicalHistory,
    CreateCurrentMedication,
    CreateSymptoms,
    UpdateVital,
    UpdateComplaint,
    UpdateDiagnosis,
    UpdateCondition,
    UpdateMedication,
    UpdateMedicalTest,
    UpdateMedicalHistory,
    UpdateCurrentMedication,
    UpdateSymptoms,
)
from core.controllers.pmr_controller import PMRController
from core import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
pmr_router = APIRouter()


@pmr_router.post("/v1/PMR/createPMR")
def createPMR(pmr_request: PMR, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/pmr/createPMR endpoint")
        logging.debug(f"Request: {pmr_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().create_pmr(request=pmr_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/createPMR endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/createPMR endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/updatePMR")
def updatePMR(pmr_request: PMR, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/pmr/updatePMR endpoint")
        logging.debug(f"Request: {pmr_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().update_pmr(request=pmr_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/updatePMR endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/updatePMR endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/createVital")
def createVital(vital_request: CreateVital, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/pmr/createVital endpoint")
        logging.debug(f"Request: {vital_request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().create_vital(request=vital_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/createVital endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/createVital endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/updateVital")
def updateVital(vital_request: UpdateVital, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/pmr/updateVital endpoint")
        logging.debug(f"Request: {vital_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().update_vital(request=vital_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/updateVital endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/updateVital endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/createCondition")
def createCondition(
    condition_request: CreateCondition, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/createCondition endpoint")
        logging.debug(f"Request: {condition_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().create_condition(request=condition_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/createCondition endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/createCondition endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/updateCondition")
def updateCondition(
    condition_request: UpdateCondition, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/updateCondition endpoint")
        logging.debug(f"Request: {condition_request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().update_condition(request=condition_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/updateCondition endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/updateCondition endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/createComplaints")
def createComplaints(
    complaint_request: CreateComplaint, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/createComplaints endpoint")
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
        logging.error(f"Error in /v1/pmr/createComplaints endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/createComplaints endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/updateComplaints")
def updateComplaints(
    complaint_request: UpdateComplaint, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/updateComplaints endpoint")
        logging.debug(f"Request: {complaint_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().update_complaints(request=complaint_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/updateComplaints endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/updateComplaints endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/createDiagnosis")
def createDiagnosis(
    diagnosis_request: CreateDiagnosis, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/createDiagnosis endpoint")
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
        logging.error(f"Error in /v1/pmr/createDiagnosis endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/createDiagnosis endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/updateDiagnosis")
def updateDiagnosis(
    diagnosis_request: UpdateDiagnosis, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/updateDiagnosis endpoint")
        logging.debug(f"Request: {diagnosis_request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().update_diagnosis(request=diagnosis_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/updateDiagnosis endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/updateDiagnosis endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/createSymptoms")
def createSymptoms(
    symptoms_request: CreateSymptoms, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/createSymptoms endpoint")
        logging.debug(f"Request: {symptoms_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().create_symptoms(request=symptoms_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/createSymptoms endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/createSymptoms endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/updateSymptoms")
def updateDiagnosis(
    symptoms_request: UpdateSymptoms, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/updateSymptoms endpoint")
        logging.debug(f"Request: {symptoms_request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().update_symptoms(request=symptoms_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/updateSymptoms endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/updateSymptoms endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/createMedication")
def createMedication(
    medication_request: CreateMedication, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/createMedication endpoint")
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
        logging.error(f"Error in /v1/pmr/createMedication endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/createMedication endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/updateMedication")
def updateMedication(
    medication_request: UpdateMedication, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/updateMedication endpoint")
        logging.debug(f"Request: {medication_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().update_medication(request=medication_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/createMedication endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/createMedication endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/createCurrentMedication")
def createCurrentMedication(
    current_medication_request: CreateCurrentMedication,
    token: str = Depends(oauth2_scheme),
):
    try:
        logging.info("Calling /v1/pmr/createCurrentMedication endpoint")
        logging.debug(f"Request: {current_medication_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().create_current_medication(
                request=current_medication_request
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/createCurrentMedication endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/createCurrentMedication endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/updateCurrentMedication")
def updateCurrentMedication(
    update_medication_request: UpdateCurrentMedication,
    token: str = Depends(oauth2_scheme),
):
    try:
        logging.info("Calling /v1/pmr/updateCurrentMedication endpoint")
        logging.debug(f"Request: {update_medication_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().update_current_medication(
                request=update_medication_request
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/updateCurrentMedication endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/updateCurrentMedication endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/createMedicalTest")
def createMedicalTest(
    medicalTest_request: CreateMedicalTest, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/createMedicalTest endpoint")
        logging.debug(f"Request: {current_medication_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().create_medicalTest(
                request=current_medication_request
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/createMedicalTest endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/createMedicalTest endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/updateMedicalTest")
def updateMedicalTest(
    medicalTest_request: UpdateMedicalTest, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/updateMedicalTest endpoint")
        logging.debug(f"Request: {medicalTest_request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().update_medicalTest(request=medicalTest_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/updateMedicalTest endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/updateMedicalTest endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/createMedicalHistory")
def createMedicalHistory(
    medical_history_request: CreateMedicalHistory, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/createMedicalHistory endpoint")
        logging.debug(f"Request: {medical_history_request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().create_medicalHistory(
                request=medical_history_request
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/createMedicalHistory endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/createMedicalHistory endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/updateMedicalHistory")
def updateMedicalHistory(
    medical_history_request: UpdateMedicalHistory, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/updateMedicalHistory endpoint")
        logging.debug(f"Request: {medical_history_request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().update_medicalHistory(
                request=medical_history_request
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/updateMedicalHistory endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/updateMedicalHistory endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/sync/{pmr_id}")
def sync_pmr_to_gateway(pmr_id: str, hip_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/pmr/sync endpoint")
        logging.debug(f"Request: {pmr_id}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
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
