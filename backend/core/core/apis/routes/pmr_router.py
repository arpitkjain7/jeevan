from fastapi import APIRouter, HTTPException, status, Depends, UploadFile
from typing import List
from collections import defaultdict
from datetime import date
from core.crud.hims_patientMedicalRecord_crud import CRUDPatientMedicalRecord
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.pmr_request import (
    CreatePMR,
    CreatePMR_UpdateConsultation,
    PMR,
    CreateVital,
    UpdateVital,
    UpdateConsultationStatus,
    FollowUp_ConsultationStatus,
    FollowUp,
    DocumentTypes,
    SendNotification,
    PrescriptionMode,
    SendNotificationByDocumentId,
    SendGoogleReview,
    SendAppointmentList,
    PMRMetadata,
)
from core.controllers.pmr_controller import PMRController
from core.controllers.appointment_controller import AppointmentsController
from core import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
pmr_router = APIRouter()


@pmr_router.post("/v1/PMR/createPMR")
def createPMR(
    pmr_request: CreatePMR,
    token: str = Depends(oauth2_scheme),
):
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


@pmr_router.post("/v2/PMR/createPMR")
def createPMR_v2(
    pmr_request: CreatePMR_UpdateConsultation,
    token: str = Depends(oauth2_scheme),
):
    try:
        logging.info("Calling /v2/PMR/createPMR endpoint")
        logging.debug(f"Request: {pmr_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().create_pmr_v2(request=pmr_request)

        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v2/PMR/createPMR endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v2/PMR/createPMR endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/submitPMR")
def submitPMR(
    pmr_request: PMR = None,
    appointment_request: FollowUp_ConsultationStatus = None,
    token: str = Depends(oauth2_scheme),
):
    try:
        logging.info("Calling /v1/pmr/submitPMR endpoint")
        logging.debug(f"Request: {pmr_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().submit_pmr_v1(
                pmr_request=pmr_request, appointment_request=appointment_request
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/submitPMR endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/submitPMR endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/previewPMR")
def previewPMR(
    pmr_metadata: PMRMetadata,
    pmr_request: PMR = None,
    appointment_request: FollowUp_ConsultationStatus = None,
    token: str = Depends(oauth2_scheme),
):
    try:
        logging.info("Calling /v1/pmr/previewPMR endpoint")
        logging.debug(f"Request: {pmr_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().preview_pmr(
                pmr_request=pmr_request,
                appointment_request=appointment_request,
                pmr_metadata=pmr_metadata,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/previewPMR endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/previewPMR endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/preview-summary")
def previewPMR(
    pmr_metadata: PMRMetadata,
    pmr_request: PMR = None,
    appointment_request: FollowUp_ConsultationStatus = None,
    token: str = Depends(oauth2_scheme),
):
    try:
        logging.info("Calling /v1/pmr/previewPMR endpoint")
        logging.debug(f"Request: {pmr_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().preview_summary(
                pmr_request=pmr_request,
                appointment_request=appointment_request,
                pmr_metadata=pmr_metadata,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/previewPMR endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/previewPMR endpoint: {error}")
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


@pmr_router.put("/v1/PMR/updateVital")
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


"""
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


@pmr_router.patch("/v1/PMR/updateCondition")
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


@pmr_router.post("/v1/PMR/createExaminationFindings")
def createExaminationFindings(
    examination_findings_request: CreateExaminationFindings,
    token: str = Depends(oauth2_scheme),
):
    try:
        logging.info("Calling /v1/pmr/createExaminationFindings endpoint")
        logging.debug(f"Request: {examination_findings_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().create_examination_findings(
                request=examination_findings_request
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/pmr/createExaminationFindings endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/createExaminationFindings endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.patch("/v1/PMR/updateExaminationFindings")
def updateExaminationFindings(
    examination_findings_request: UpdateExaminationFindings,
    token: str = Depends(oauth2_scheme),
):
    try:
        logging.info("Calling /v1/pmr/updateExaminationFindings endpoint")
        logging.debug(f"Request: {examination_findings_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().update_examination_findings(
                request=examination_findings_request
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/pmr/updateExaminationFindings endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/updateExaminationFindings endpoint: {error}")
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


@pmr_router.patch("/v1/PMR/updateDiagnosis")
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


@pmr_router.patch("/v1/PMR/updateSymptoms")
def updateSymptoms(
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


@pmr_router.patch("/v1/PMR/updateMedication")
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


@pmr_router.patch("/v1/PMR/updateCurrentMedication")
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


@pmr_router.post("/v1/PMR/createLabInvestigation")
def createLabInvestigation(
    labInvestigation_request: CreateLabInvestigation,
    token: str = Depends(oauth2_scheme),
):
    try:
        logging.info("Calling /v1/pmr/createLabInvestigation endpoint")
        logging.debug(f"Request: {labInvestigation_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().create_labInvestigation(
                request=labInvestigation_request
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/createLabInvestigation endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/createLabInvestigation endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.patch("/v1/PMR/updateMedicalTest")
def updateMedicalTest(
    medicalTest_request: UpdateLabInvestigation, token: str = Depends(oauth2_scheme)
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


@pmr_router.patch("/v1/PMR/updateMedicalHistory")
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


@pmr_router.post("/v1/PMR/addAdvice")
def addAdvice(advice_request: Advice, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/pmr/addAdvice endpoint")
        logging.debug(f"Request: {advice_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().create_advice(request=advice_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/addAdvice endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/addAdvice endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/addNotes")
def addNotes(notes_request: Notes, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/pmr/addNotes endpoint")
        logging.debug(f"Request: {notes_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().create_notes(request=notes_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/addNotes endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/addNotes endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
"""


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


@pmr_router.delete("/v1/PMR/delete/{condition_id}")
def delete_condition(condition_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/pmr/deleteCondition endpoint")
        logging.debug(f"Request: {condition_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().delete_condition(condition_id=condition_id)
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


@pmr_router.put("/v1/PMR/updateConsultationStatus")
def updateConsultationStatus(
    consultation_request: UpdateConsultationStatus, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/pmr/updateConsultationStatus endpoint")
        logging.debug(f"Request: {consultation_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().update_consultation_status(
                request=consultation_request
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/pmr/updateConsultationStatus endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/updateConsultationStatus endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.put("/v1/PMR/updateFollowUp")
def updateFollowUp(followup_request: FollowUp, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/pmr/updateFollowUp endpoint")
        logging.debug(f"Request: {followup_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().update_followup(request=followup_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/updateFollowUp endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/updateFollowUp endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/uploadDocument")
async def uploadDocument(
    pmr_id: str,
    document_type: DocumentTypes,
    files: List[UploadFile],
    token: str = Depends(oauth2_scheme),
):
    try:
        logging.info("Calling /v1/PMR/uploadDocument endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return await PMRController().upload_document(
                pmr_id=pmr_id, document_type=document_type, files=files
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/event/addCoverPhoto endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/event/addCoverPhoto endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/uploadPrescription")
async def uploadPrescription(
    pmr_id: str,
    files: List[UploadFile],
    mode: PrescriptionMode,
    token: str = Depends(oauth2_scheme),
):
    try:
        logging.info("Calling /v1/PMR/uploadPrescription endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            file_bytes = []
            for file in files:
                file_bytes.append(await file.read())
            return PMRController().upload_prescription(
                pmr_id=pmr_id, mode=mode.value, files=file_bytes
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/event/uploadPrescription endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/event/uploadPrescription endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.get("/v1/PMR/listDocuments/{pmr_id}")
def listDocuments(pmr_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/PMR/listDocuments/{pmr_id} endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().list_documents(pmr_id=pmr_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/PMR/listDocuments/{pmr_id} endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/PMR/listDocuments/{pmr_id} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.get("/v1/PMR/getDocument/{document_id}")
def getDocument(document_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/PMR/getDocument/{document_id} endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().get_document(document_id=document_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/PMR/getDocument/{document_id} endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/PMR/getDocument/{document_id} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.get("/v1/PMR/getDocumentBytes/{document_id}")
def getDocument(document_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/PMR/getDocument/{document_id} endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().get_document_bytes(document_id=document_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/PMR/getDocument/{document_id} endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/PMR/getDocument/{document_id} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


## test2
@pmr_router.post("/v1/PMR/uploadHealthDocuments")
async def uploadHealthDocuments(
    patient_id: str,
    appointment_id: str,
    hip_id: str,
    doc_ids: List[str],
    document_types: List[str],
    dates: List[date],
    files: List[UploadFile],
    token: str = Depends(oauth2_scheme),
):
    try:
        # Authenticate user
        authenticated_user_details = decodeJWT(token)
        if not authenticated_user_details:
            raise HTTPException(status_code=401, detail="Invalid access token")
        documents = defaultdict(list)
        response = []
        # Group files, document types and dates
        for file, document_type, document_date, doc_id in zip(
            files,
            document_types,
            dates,
            doc_ids,
        ):
            documents[f"{document_type}_{doc_id}_{document_date}"].append(
                {"file": file}
            )
            logging.info(f"{documents=}")
        for key, value in documents.items():
            logging.info(f"{key=}--{value=}")
            document_type, doc_id, document_date = key.split("_")
            document_list = value
            logging.info(f"{document_type=}--{doc_id=}--{document_date=}")
            pmr_docs = []
            pmr_request = {
                "patient_id": patient_id,
                "appointment_id": appointment_id,
                "hip_id": hip_id,
                "doc_id": doc_id,
            }
            pmr_id = PMRController().create_pmr(pmr_request)
            # Process each file
            for document in document_list:
                logging.info(f"{document=}")
                file = document["file"]
                file_name = file.filename
                content = await file.read()
                pmr_doc = {
                    "doc_id": doc_id,
                    "document_type": document_type,
                    "date": document_date,
                    "file": content,
                    "file_name": file_name,
                }
                pmr_docs.append(pmr_doc)
                # logging.info(f"{pmr_docs=}")
            for document in pmr_docs:
                # logging.info(f"{document=}")
                resp = PMRController().upload_health_document(
                    pmr_id=pmr_id["pmr_id"],
                    patient_id=patient_id,
                    document_data=document["file"],
                    document_type=document["document_type"],
                    document_name=document["file_name"],
                    date=document_date,
                )
                response.append(resp)
        return response
    except HTTPException as httperror:
        logging.error(f"Error in /v1/PMR/uploadHealthDocument endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/PMR/uploadHealthDocument endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/getFHIR/{pmr_id}")
def getFHIR(pmr_id: str, mode: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/PMR/getFHIR/{pmr_id} endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().get_fhir(pmr_id=pmr_id, mode=mode)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/PMR/getFHIR/{pmr_id} endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/PMR/getFHIR/{pmr_id} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v0.5/patients/sms/on-notify")
def patient_sms_on_notify(sms_on_notify_request: dict):
    try:
        logging.info("Calling /v0.5/patients/sms/on-notify endpoint")
        logging.debug(f"Request: {sms_on_notify_request}")
        return PMRController().deep_link_ack(request=sms_on_notify_request)
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


@pmr_router.post("/v1/PMR/sendNotification")
def pmr_send_notification(
    send_notification_request: SendNotification, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/PMR/sendNotification endpoint")
        logging.debug(f"Request: {send_notification_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().send_notification(request=send_notification_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/PMR/sendNotification endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/PMR/sendNotification endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/sendDocument")
def pmr_send_notification(
    send_notification_request: SendNotificationByDocumentId,
    token: str = Depends(oauth2_scheme),
):
    try:
        logging.info("Calling /v1/PMR/sendDocument endpoint")
        logging.debug(f"Request: {send_notification_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().send_notification_by_documentId(
                request=send_notification_request
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/PMR/sendDocument endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/PMR/sendDocument endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/sendGoogleReviewLink")
def pmr_send_notification(
    send_google_link_request: SendGoogleReview,
    token: str = Depends(oauth2_scheme),
):
    try:
        logging.info("Calling /v1/PMR/sendGoogleReviewLink endpoint")
        logging.debug(f"Request: {send_google_link_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PMRController().send_google_review_link(
                request=send_google_link_request
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/PMR/sendGoogleReviewLink endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/PMR/sendGoogleReviewLink endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/v1/PMR/sendAppointementList")
def pmr_send_notification(
    send_appointment_list_request: SendAppointmentList,
):
    try:
        logging.info("Calling /v1/PMR/sendGoogleReviewLink endpoint")
        logging.debug(f"Request: {send_appointment_list_request}")
        return PMRController().send_appointment_list(
            request=send_appointment_list_request
        )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/PMR/sendGoogleReviewLink endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/PMR/sendGoogleReviewLink endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@pmr_router.post("/test123")
def test(pmr_id: str):
    try:
        return CRUDPatientMedicalRecord().read_joined(pmr_id=pmr_id)
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
