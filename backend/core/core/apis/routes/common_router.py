from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from core.controllers.common_controller import Common
from core.apis.schemas.requests.doctor_request import (
    UpdateDoctor,
    DocDetails,
    ExternalDoc,
    DocDetailsV2,
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


@common_router.post("/v1/doctor-details/create")
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
        logging.info(f"Calling /v1/doctor-details/create")
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
        logging.error(f"Error in /v1/doctor-details/create: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/doctor-details/create: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@common_router.post("/v1/doctor-details/check-endpoint-availability")
def check_endpoint_availability(
    endpoint: str,
    token: str = Depends(oauth2_scheme),
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
        logging.info(f"Calling /v1/doctor-details/check-endpoint-availability")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return Common().check_endpoint_availability(endpoint=endpoint)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/doctor-details/check-endpoint-availability: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(
            f"Error in /v1/doctor-details/check-endpoint-availability: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@common_router.get("/v1/doctor-details/get-doctor-profile/{endpoint}")
def get_doctor_profile_details(
    endpoint: str,
    token: str = Depends(oauth2_scheme),
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
        logging.info(f"Calling /v1/doctor-details/get-doctor-profile")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            doctor_details_obj = Common().get_doctor_profile_details(endpoint=endpoint)
            if doctor_details_obj:
                return doctor_details_obj
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No record found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/doctor-details/get-doctor-profile: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/doctor-details/get-doctor-profile : {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@common_router.post("/v2/doctor-details/create")
def create_doctor(request: DocDetailsV2, token: str = Depends(oauth2_scheme)):
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
        logging.info(f"Calling /v2/doctor-details/create")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return Common().v2_create_doctor(request=request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v2/doctor-details/create: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v2/doctor-details/create: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@common_router.post("/v1/doctor-details/update")
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
        logging.info(f"Calling /v1/doctor-details/update")
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
        logging.error(f"Error in /v1/doctor-details/update: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/doctor-details/update: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@common_router.get("/v1/doctor-details/list-all")
def get_all_doctors(hip_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/doctor-details/list-all")
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
        logging.error(f"Error in /v1/doctor-details/list-all endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/doctor-details/list-all endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@common_router.get("/v1/doctor-details/get-by-id/{doc_id}")
def get_all_doctors(doc_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/doctor-details/get-by-id/{doc_id}")
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
        logging.error(
            f"Error in /v1/doctor-details/get-by-id/{doc_id} endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(
            f"Error in /v1/doctor-details/get-by-id/{doc_id} endpoint: {error}"
        )
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
