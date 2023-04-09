from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from core.controllers.listOfDiagnosis_controller import ListOfDiagnosisController
from commons.auth import decodeJWT
from fastapi.security import OAuth2PasswordRequestForm
from core import logger

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
listOfComplaint_router = APIRouter()


@listOfComplaint_router.post(
    "/v1/listOfComplaints/create",
)
def add_complaint(complaint: str, token: str = Depends(oauth2_scheme)):
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
        logging.info("Calling /v1/listOfComplaints/create")
        logging.debug(f"Request: {complaint}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfComplaintsController().add_complaint_controller(complaint)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/listOfComplaints/create endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfComplaints/create endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfComplaint_router.get("/v1/listOfComplaints/getAll")
def get_all_complaint(token: str = Depends(oauth2_scheme)):
    """[Get List of all Users]
    Raises:
        error: [Error details]
    Returns:
        [list]: [List of Users]
    """
    try:
        logging.info("Calling /v1/listOfComplaints/getAll endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfComplaintsController().get_all_complaints_controller()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/listOfComplaints/getAll endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfComplaints/getAll endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfComplaint_router.post("/v1/listOfComplaints/delete")
def delete_complaint(complaint_id: int, token: str = Depends(oauth2_scheme)):
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
        logging.info("Calling /v1/listOfComplaints/delete")
        logging.debug(f"Request: {complaint_id}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfComplaintsController().delete_complaint_controller(
                complaint_id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/listOfComplaints/delete endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfComplaints/delete endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
