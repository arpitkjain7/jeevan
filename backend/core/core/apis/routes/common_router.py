from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from core.controllers.common_controller import Common
from core.controllers.patient_controller import PatientController
from core.controllers.appointment_controller import AppointmentsController
from core.apis.schemas.requests.doctor_request import (
    ExternalDoc,
)
from core.apis.schemas.requests.hip_request import DeepLinkNotify
from core.apis.schemas.requests.appointment_request import BookAppointment, Create
from core.apis.schemas.requests.patient_request import RegisterPatientV3
from commons.auth import decodeJWT
from fastapi.security import OAuth2PasswordRequestForm
from core import logger


logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
common_router = APIRouter()

"""listOfComplaint_router = APIRouter()
listOfDiagnosis_router = APIRouter()
listOfMedicalTests_router = APIRouter()
listOfMedicines_router = APIRouter()
"""


# below API is not showing in API lists


@common_router.post("/v1/deepLinkNotify")
def deep_link_notify(
    deep_link_request: DeepLinkNotify, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info(f"Calling /v1/deepLinkNotify endpoint")
        logging.debug(f"Request: {deep_link_request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return Common().deep_link_notify(
                mobile_no=deep_link_request.mobile_no,
                hip_id=deep_link_request.hip_id,
                hip_name=deep_link_request.hip_name,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/deepLinkNotify endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/deepLinkNotify endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


# TODO: need to remove the APIs once FE changes are completed
@common_router.get("/v1/listAllDoctors")
def get_all_doctors(hip_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/listAllDoctors")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return Common().get_all_doctors(hip_id=hip_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/listAllDoctors endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listAllDoctors endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@common_router.get("/v1/getDoctorDetails")
def get_all_doctors(doc_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/getDoctorDetails")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return Common().doctor_details_by_docId(doc_id=doc_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/getDoctorDetails endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/getDoctorDetails endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


#### function to add external doctor
@common_router.post("/v1/doctor-details/addExternal")
def create_external_doctor(request: ExternalDoc, token: str = Depends(oauth2_scheme)):
    """[API router to register new user into the system]
    Args:
        register_user_request (Register): [New user details]
    Raises:
        HTTPException: [Unauthorized exception when invalid token is passed]
        error: [Exception in underlying controller]
    Returns:
        [RegisterResponse]: [Register new user response]
    """
    try:
        logging.info(f"Calling /v1/doctor-details/addExternal")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return Common().create_doctor(request=request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/doctor-details/addExternal: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/doctor-details/addExternal: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@common_router.post("/v1/register-patient/book-appointment")
def create_appointment(request: BookAppointment):
    """[API router to register new user into the system]
    Args:
        register_user_request (Register): [New user details]
    Raises:
        HTTPException: [Unauthorized exception when invalid token is passed]
        error: [Exception in underlying controller]
    Returns:
        [RegisterResponse]: [Register new user response]
    """
    try:
        logging.info("Calling /v1/register-patient/book-appointment")
        request_dict = request.dict()
        logging.info(f"{request_dict=}")
        logging.info("Preparing patient register request")
        patient_register_request = RegisterPatientV3(
            **{
                "mobile_number": request_dict.get("mobile_number"),
                "name": request_dict.get("name"),
                "gender": request_dict.get("gender"),
                "DOB": request_dict.get("DOB"),
                "age": request_dict.get("age"),
                "hip_id": request_dict.get("hip_id"),
            }
        )
        registered_patient_obj = PatientController().register_patient_v3_controller(
            request=patient_register_request
        )
        logging.info("Preparing appointment create request")
        appointment_create_request = Create(
            **{
                "doc_id": request_dict.get("doc_id"),
                "patient_id": registered_patient_obj.get("id"),
                "appointment_type": "first visit",
                "encounter_type": "inpatient encounter",
                "hip_id": request_dict.get("hip_id"),
                "appointment_start": request_dict.get("appointment_start"),
                "appointment_end": request_dict.get("appointment_end"),
            }
        )
        created_appointment_obj = AppointmentsController().create_appointment(
            request=appointment_create_request
        )
        created_appointment_obj.update({"patient_id": registered_patient_obj.get("id")})
        return created_appointment_obj
    except Exception as error:
        logging.error(f"Error in /v1/register-patient/book-appointment : {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
