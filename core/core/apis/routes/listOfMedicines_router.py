from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from core.controllers.listOfMedicines_controller import ListOfMedicinesController
from commons.auth import decodeJWT
from fastapi.security import OAuth2PasswordRequestForm
from core import logger

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
listOfMedicines_router = APIRouter()


@listOfMedicines_router.post(
    "/v1/listOfMedicines/addMedicine",
)
def add_medicine(name: str, company: str, token: str = Depends(oauth2_scheme)):
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
        logging.info("Calling /v1/listOfMedicine/addMedicine")
        logging.debug(f"Request: {name}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfMedicinesController().add_medicine_controller(
                name,
                company,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/listOfMedicines/addMedicine endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfMedicines/addMedicine endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfMedicines_router.get("/v1/listOfMedicines/getAllMedicines")
def get_all_medicines(token: str = Depends(oauth2_scheme)):
    """[Get List of all Users]
    Raises:
        error: [Error details]
    Returns:
        [list]: [List of Users]
    """
    try:
        logging.info("Calling /v1/listOfMedicines/getAllMedicines endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfMedicinesController().get_all_medicines_controller()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/listOfMedicines/getAllMedicines endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfMedicines/getAllMedicines endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfMedicines_router.post("/v1/listOfMedicines/deleteMedicine")
def delete_medicine(medicine_id: int, token: str = Depends(oauth2_scheme)):
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
        logging.info("Calling /v1/listOfMedicines/deleteMedicine")
        logging.debug(f"Request: {test_id}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfMedicinesController().delete_medicine_controller(medicine_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/listOfMedicines/deleteMedicine endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfMedicines/deleteMedicine endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
