from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from core.controllers.listOfDiagnosis_controller import ListOfDiagnosisController
from commons.auth import decodeJWT
from fastapi.security import OAuth2PasswordRequestForm
from core import logger

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
listOfDiagnosis_router = APIRouter()


@listOfDiagnosis_router.post(
    "/v1/listOfDiagnosis/addDisease",
)
def add_disease(disease: str, token: str = Depends(oauth2_scheme)):
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
        logging.debug(f"Request: {disease}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfDiagnosisController().add_disease_controller(disease)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/listOfDiagnosis/create endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfDiagnosis/create endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfDiagnosis_router.get("/v1/listOfDiagnosis/getAllDiseases")
def get_all_diseases(token: str = Depends(oauth2_scheme)):
    """[Get List of all Users]
    Raises:
        error: [Error details]
    Returns:
        [list]: [List of Users]
    """
    try:
        logging.info("Calling /v1/listOfDiagnosis/getAllDiseases endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfDiagnosisController().get_all_diseases_controller()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/listOfDiagnosis/getAllDiseases endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfDiagnosis/getAllDiseases endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@listOfDiagnosis_router.post("/v1/listOfDiagnosis/deleteDisease")
def delete_disease(disease_id: int, token: str = Depends(oauth2_scheme)):
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
        logging.info("Calling /v1/listOfDiagnosis/deleteDisease")
        logging.debug(f"Request: {disease_id}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return ListOfDiagnosisController().delete_disease_controller(disease_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/listOfDiagnosis/deleteDisease endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/listOfDiagnosis/deleteDisease endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
