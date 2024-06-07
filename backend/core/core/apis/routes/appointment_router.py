from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.appointment_request import Create, Update, Read
from core.controllers.appointment_controller import AppointmentsController
from commons.auth import decodeJWT
from fastapi.security import OAuth2PasswordRequestForm
from core import logger

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
appointment_router = APIRouter()


@appointment_router.post("/v1/appointment/create")
def create_appointment(
    create_appointment_request: Create, token: str = Depends(oauth2_scheme)
):
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
        logging.info("Calling /v1/appointment/create")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return AppointmentsController().create_appointment(
                request=create_appointment_request
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/appointment/create: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/appointment/create: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@appointment_router.get("/v1/appointment/listAll")
def get_appointment(hip_id: str, token: str = Depends(oauth2_scheme)):
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
        logging.info(f"Calling /v1/appointment/listAll")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return AppointmentsController().get_all_appointment(hip_id=hip_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in  /v1/appointment/listAll: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in  /v1/appointment/listAll: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@appointment_router.get("/v1/appointment/listByDate")
def get_appointment_by_date(
    hip_id: str, appointment_date: str, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info(f"Calling /v1/appointment/listByDate")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return AppointmentsController().get_all_appointments_by_date(
                hip_id=hip_id, appointment_date=appointment_date
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/appointment/listByDate: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/appointment/listByDate: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@appointment_router.get("/v1/appointment/listFollowUpByDate")
def get_followups_by_date(appointment_date: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/appointment/listFollowUpByDate")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return AppointmentsController().get_all_followups_by_date(
                appointment_date=appointment_date
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/appointment/listFollowUpByDate: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/appointment/listFollowUpByDate: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@appointment_router.get("/v1/appointment/{doc_id}")
def get_appointment_by_docId(
    doc_id: str, hip_id: str, token: str = Depends(oauth2_scheme)
):
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
        logging.info(f"Calling /v1/appointment/{doc_id}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return AppointmentsController().get_appointment_by_doc_id(
                doc_id=doc_id, hip_id=hip_id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in  /v1/appointment/{doc_id}: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in  /v1/appointment/{doc_id}: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@appointment_router.get("/v1/slots/{doc_id}")
def get_slots_by_docId(
    doc_id: str, appointment_date: str, hip_id: str, token: str = Depends(oauth2_scheme)
):
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
        logging.info(f"Calling /v1/slots/{doc_id}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return AppointmentsController().get_slots(
                doc_id=doc_id, appointment_date=appointment_date, hip_id=hip_id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/slots/{doc_id}: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/slots/{doc_id}: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@appointment_router.delete("/v1/slots/{slot_id}")
def delete_slot(slot_id: int, token: str = Depends(oauth2_scheme)):
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
        logging.info(f"Calling /v1/slots/{slot_id}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return AppointmentsController().delete_slots(slot_id=slot_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/slots/{slot_id}: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/slots/{slot_id}: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@appointment_router.patch("/v1/slots/update")
def update_slot(request: Update, token: str = Depends(oauth2_scheme)):
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
        logging.info(f"Calling /v1/slots/update")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return AppointmentsController().update_slots(request=request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/slots/update: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/slots/update: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@appointment_router.get("/v1/appointmentAnalytics")
def get_appointment_analystics(hip_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/appointmentAnalytics")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return AppointmentsController().get_appointment_metadata(hip_id=hip_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/appointmentAnalytics: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/appointmentAnalytics: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
