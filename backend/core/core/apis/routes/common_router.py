from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from core.controllers.common_controller import Common
from core.apis.schemas.requests.doctor_request import (
    UpdateDoctor,
    DocDetails,
    ExternalDoc,
)
from core.apis.schemas.requests.template_request import TemplateDetails
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
def deep_link_notify(mobile_no: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/deepLinkNotify endpoint")
        logging.debug(f"Request: {mobile_no=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return Common().deep_link_notify(mobile_no=mobile_no)
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


@common_router.post("/v1/createTemplate")
def create_template(request: TemplateDetails, token: str = Depends(oauth2_scheme)):
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
        logging.info(f"Calling /v1/createTemplate")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return Common().create_template(request=request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/createTemplate: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/createTemplate: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@common_router.get("/v1/getTemplate/{template_id}")
def get_template_by_id(template_id: int, token: str = Depends(oauth2_scheme)):
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
        logging.info(f"Calling /v1/get_template_by_id")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return Common().get_template_by_id(template_id=template_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/get_template_by_id: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/get_template_by_id: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@common_router.get("/v1/getTemplate/")
def get_template_by_type(
    template_name: str = None,
    template_type: str = None,
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
        logging.info(f"Calling /v1/get_template_by_type")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return Common().get_template_by_type(type=template_type, name=template_name)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/get_template_by_type: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/get_template_by_type: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@common_router.get("/v1/getAllTemplate")
def get_all_template(token: str = Depends(oauth2_scheme)):
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
        logging.info(f"Calling /v1/get_all_template")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return Common().get_all_template()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/get_all_template: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/get_all_template: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
