from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.patient_request import (
    FetchRegisterationMode,
    AuthInit,
    VerifyOtp,
    VerifyDemographic,
    RegisterWithoutABHA,
    UpdatePatient,
)
from core.apis.schemas.requests.vital_request import Read, VitalType
from core.controllers.patient_controller import PatientController
from core import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
patient_router = APIRouter()


@patient_router.get("/v1/patient/verifyAbha")
def verify_ABHA(
    health_id: str, year_of_birth: str, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info(f"Calling /v1/verifyAbha endpoint")
        logging.debug(f"Request: {health_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PatientController().abha_verification(
                health_id=health_id,
                year_of_birth=year_of_birth,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/verifyAbha endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/verifyAbha endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@patient_router.post("/v1/patient/updateAbhaAddress")
def update_abha_address(
    patient_id: str, abha_address: str, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info(f"Calling /v1/patient/updateAbhaAddress endpoint")
        logging.debug(f"Request: {abha_address=}")
        logging.debug(f"Request: {patient_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PatientController().abha_address_update(
                patient_id=patient_id,
                abha_address=abha_address,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/patient/updateAbhaAddress endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/patient/updateAbhaAddress endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@patient_router.post("/v1/patient/fetchModes")
def fetch_auth_modes(
    request: FetchRegisterationMode, token: str = Depends(oauth2_scheme)
):
    pass
    try:
        logging.info("Calling /v1/patient/fetchModes endpoint")
        logging.debug(f"Request: {request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PatientController().fetch_auth_modes(request=request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/patient/fetchModes endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/patient/fetchModes endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@patient_router.post("/v1/patient/auth/init")
def auth_init(request: AuthInit, token: str = Depends(oauth2_scheme)):
    pass
    try:
        logging.info("Calling /v1/patient/auth/init endpoint")
        logging.debug(f"Request: {request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PatientController().auth_init(request=request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/patient/auth/init endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/patient/auth/init endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@patient_router.post("/v1/patient/auth/verifyOtp")
def auth_verifyOtp(request: VerifyOtp, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/patient/auth/verifyOtp endpoint")
        logging.debug(f"Request: {request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PatientController().verify_otp(request=request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/patient/auth/verifyOtp endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/patient/auth/verifyOtp endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@patient_router.post("/v1/patient/auth/verifyDemographic")
def auth_verifyDemographic(
    request: VerifyDemographic, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/patient/auth/verifyDemographic endpoint")
        logging.debug(f"Request: {request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PatientController().verify_demographic(request=request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/patient/auth/verifyDemographic endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/patient/auth/verifyDemographic endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@patient_router.post("/v1.0/patients/profile/share")
async def patient_profileShare(request: Request):
    try:
        logging.info("Calling /v1.0/patients/profile/share endpoint")
        hip_id = request.headers.get("X-HIP-ID")
        request_json = await request.json()
        logging.debug(f"Request: {request_json}")
        return PatientController().patient_share(request=request_json, hip_id=hip_id)
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


@patient_router.post("/v0.5/care-contexts/discover")
async def discover_patient(request: Request):
    try:
        logging.info("Calling /v0.5/care-contexts/discover endpoint")
        hip_id = request.headers.get("X-HIP-ID")
        logging.debug(f"hip_id: {hip_id}")
        request_json = await request.json()
        logging.debug(f"Request: {request_json}")
        return PatientController().discover_patient(request=request_json, hip_id=hip_id)
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


@patient_router.post("/v0.5/links/link/init")
async def link_patient(request: Request):
    try:
        logging.info("Calling /v0.5/links/link/init endpoint")
        hip_id = request.headers.get("X-HIP-ID")
        logging.debug(f"hip_id: {hip_id}")
        request_json = await request.json()
        logging.debug(f"Request: {request_json}")
        return PatientController().link_patient(request=request_json, hip_id=hip_id)
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


@patient_router.post("/v0.5/links/link/confirm")
async def link_on_confirm(request: Request):
    try:
        logging.info("Calling /v0.5/links/link/confirm endpoint")
        hip_id = request.headers.get("X-HIP-ID")
        logging.debug(f"hip_id: {hip_id}")
        request_json = await request.json()
        logging.debug(f"Request: {request_json}")
        return PatientController().link_confirm(request=request_json, hip_id=hip_id)
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


@patient_router.post("/v1/patient/register")
def register_patient(
    register_patient_request: RegisterWithoutABHA, token: str = Depends(oauth2_scheme)
):
    """[API router to register new patient into the system]
    Args:
        register_patient_request (Register): [New user details]
    Raises:
        HTTPException: [Unauthorized exception when invalid token is passed]
        error: [Exception in underlying controller]
    Returns:
        [RegisterResponse]: [Register new user response]
    """
    try:
        logging.info("Calling /v1/patient/register endpoint")
        logging.debug(f"Request: {register_patient_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PatientController().register_patient_controller(
                register_patient_request
            )
            # if patient_obj.get("patient_id") is None:
            #     raise HTTPException(
            #         status_code=status.HTTP_400_BAD_REQUEST,
            #         detail=patient_obj["status"],
            #     )
            # else:
            #     return patient_obj
    except HTTPException as httperror:
        logging.error(f"Error in /v1/patient/register endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/patient/register endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@patient_router.post("/v1/patient/update")
def updatePatient(update_patient: UpdatePatient, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/patient/update endpoint")
        logging.debug(f"Request: {update_patient}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PatientController().update_patient(request=update_patient)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/patient/update endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/patient/update endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@patient_router.get("/v1/patient/listAll")
def list_all_patients(hip_id: str, token: str = Depends(oauth2_scheme)):
    """[API router to list all patient into the system]
    Raises:
        HTTPException: [Unauthorized exception when invalid token is passed]
        error: [Exception in underlying controller]
    Returns:
        [RegisterResponse]: [Register new user response]
    """
    try:
        logging.info("Calling /v1/patient/listAll endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PatientController().list_all_patients(hip_id=hip_id)
    except HTTPException as httperror:
        logging.error(f"Error in /v1/patient/listAll endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/patient/listAll endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@patient_router.get("/v1/patient/getVitals")
def get_vital(
    patient_id: str, vital_type: VitalType, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info(f"Calling /v1/pmr/get_vital endpoint")
        logging.debug(f"Request: {vital_type.name=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PatientController().get_vital(
                patient_id=patient_id, vital_type=vital_type.name
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/pmr/get_vital endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/pmr/get_vital endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@patient_router.get("/v1/patient/{patient_id}")
def get_patient_details(patient_id: str, token: str = Depends(oauth2_scheme)):
    """[API router to list all patient into the system]
    Raises:
        HTTPException: [Unauthorized exception when invalid token is passed]
        error: [Exception in underlying controller]
    Returns:
        [RegisterResponse]: [Register new user response]
    """
    try:
        logging.info("Calling /v1/patient/get_details endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return PatientController().get_patient_details(patient_id=patient_id)
    except HTTPException as httperror:
        logging.error(f"Error in /v1/patient/listAll endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/patient/listAll endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
