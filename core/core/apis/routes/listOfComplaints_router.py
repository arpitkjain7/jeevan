from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from core.controllers.listOfComplaint_controller import ListOfComplaintsController
from commons.auth import decodeJWT
from fastapi.security import OAuth2PasswordRequestForm
from core import logger

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
listOfComplaint_router = APIRouter()


@listOfComplaint_router.post("/v1/addNewComplaint")
def add_complaint(complaint: str):
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
        logging.info("Calling /v1/add_new_complaint")
        logging.debug(f"Request: {complaint}")

        return ListOfComplaintsController().add_complaint_controller(
            complaint
        )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/add_new_complaint endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/add_new_complaint endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )

@listOfComplaint_router.get("/v1/complaint/list")
def get_all_complaint():
    """[Get List of all Users]
    Raises:
        error: [Error details]
    Returns:
        [list]: [List of Users]
    """
    try:
        logging.info("Calling /v1/complaint/list endpoint")
        return ListOfComplaintsController().get_all_complaints_controller()
    except HTTPException as httperror:
        logging.error(f"Error in /v1/complaint/list endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/complaint/list endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfComplaint_router.post("/v1/delete_complaint_id")
def delete_complaint(complaint_id: int):
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
        logging.info("Calling /v1/delete_complaint_id")
        logging.debug(f"Request: {complaint_id}")

        return ListOfComplaintsController().delete_complaint_controller(
            complaint_id
        )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/delete_complaint endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/delete_complaint endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )