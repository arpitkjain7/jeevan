from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from core.controllers.common_controller import Common
from core.apis.schemas.requests.doctor_request import (
    UpdateDoctor,
    DocDetails,
    ExternalDoc,
)
from core.apis.schemas.requests.hip_request import DeepLinkNotify
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


@common_router.post("/v1/doctorDetails/create")
def create_doctor(request: DocDetails, token: str = Depends(oauth2_scheme)):
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
        logging.info(f"Calling /v1/doctorDetails/create")
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
        logging.error(f"Error in /v1/doctorDetails/create: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/doctorDetails/create: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@common_router.post("/v1/doctorDetails/update")
def update_doc_details(request: UpdateDoctor, token: str = Depends(oauth2_scheme)):
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
        logging.info(f"Calling /v1/doctorDetails/update")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return Common().update_doc_details(request=request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/doctorDetails/update: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/doctorDetails/update: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


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


#### function to add external doctor
@common_router.post("/v1/doctorDetails/addExternal")
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
        logging.info(f"Calling /v1/doctorDetails/addExternal")
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
        logging.error(f"Error in /v1/doctorDetails/addExternal: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/doctorDetails/addExternal: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
