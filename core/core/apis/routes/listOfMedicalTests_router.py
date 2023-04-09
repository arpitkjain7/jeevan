from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from core.controllers.listOfMedicalTests_controller import ListOfMedicalTestsController
from commons.auth import decodeJWT
from fastapi.security import OAuth2PasswordRequestForm
from core import logger

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
listOfMedicalTests_router = APIRouter()


@listOfMedicalTests_router.post(
    "/v1/listOfMedicalTests/addMedicalTest",
)
def add_medical_test(medicalTest: str, token: str = Depends(oauth2_scheme)):
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
        logging.info("Calling /v1/listOfMedicalTests/addMedicalTest")
        logging.debug(f"Request: {medicalTest}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfMedicalTestsController().add_medicalTest_controller(
                medicalTest
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/listOfMedicalTests/addMedicalTest endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(
            f"Error in /v1/listOfMedicalTests/addMedicalTest endpoint: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfMedicalTests_router.get("/v1/listOfMedicalTest/getAllTests")
def get_all_medical_tests(token: str = Depends(oauth2_scheme)):
    """[Get List of all Users]
    Raises:
        error: [Error details]
    Returns:
        [list]: [List of Users]
    """
    try:
        logging.info("Calling /v1/listOfMedicalTest/getAllTests endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfMedicalTestsController().get_all_tests_controller()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/listOfMedicalTest/getAllTests endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfMedicalTest/getAllTests endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfMedicalTests_router.post("/v1/listOfMedicalTest/deleteTest")
def delete_medical_test(test_id: int, token: str = Depends(oauth2_scheme)):
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
        logging.info("Calling /v1/listOfMedicalTest/deleteTest")
        logging.debug(f"Request: {test_id}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfMedicalTestsController().delete_test_controller(test_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/listOfMedicalTest/deleteTest endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfMedicalTest/deleteTest endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
