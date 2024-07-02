from fastapi import APIRouter, HTTPException, status, Depends, UploadFile
from fastapi.security import OAuth2PasswordBearer
from core.controllers.doctor_controller import DoctorController
from core.apis.schemas.requests.doctor_request import (
    UpdateDoctor,
    DocDetails,
    ExternalDoc,
    DocDetailsV2,
)
from commons.auth import decodeJWT
from core import logger
import base64

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
doctor_router = APIRouter()


@doctor_router.post("/v1/doctor-details/create")
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
            return DoctorController().create_doctor(request=request)
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


@doctor_router.post("/v1/doctor-details/check-endpoint-availability")
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
            return DoctorController().check_endpoint_availability(endpoint=endpoint)
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


@doctor_router.get("/v1/doctor-details/get-doctor-profile/{endpoint}")
def get_doctor_profile_details(
    endpoint: str,
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
        doctor_details_obj = DoctorController().get_doctor_profile_details(
            endpoint=endpoint
        )
        if doctor_details_obj:
            return doctor_details_obj
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No record found",
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


@doctor_router.post("/v2/doctor-details/create")
def create_doctor_v2(
    request: DocDetailsV2,
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
        logging.info(f"Calling /v2/doctor-details/create")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return DoctorController().v2_create_doctor(request=request)
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


@doctor_router.post("/v2/doctor-details/profile-photo-signature-upload")
async def upload_profile_photo_and_signature(
    doc_id: str,
    profile_photo: UploadFile = None,
    signature: UploadFile = None,
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
        logging.info(f"Calling /v2/doctor-details/profile-photo-signature-upload")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            request = {"id": doc_id}
            if profile_photo:
                contents = await profile_photo.read()
                profile_encoded_content = base64.b64encode(contents).decode("utf-8")
                request.update({"profile_photo": profile_encoded_content})
            if signature:
                contents = await signature.read()
                # Create signature bytes
                sign_encoded_content = base64.b64encode(contents).decode("utf-8")
                request.update({"signature": sign_encoded_content})
            return DoctorController().update_profile_photo_signature(request=request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v2/doctor-details/profile-photo-signature-upload : {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(
            f"Error in /v2/doctor-details/profile-photo-signature-upload : {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@doctor_router.post("/v1/doctor-details/update")
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
            return DoctorController().update_doc_details(request=request)
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


@doctor_router.get("/v1/doctor-details/list-all")
def get_all_doctors(hip_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/doctor-details/list-all")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return DoctorController().get_all_doctors(hip_id=hip_id)
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


@doctor_router.get("/v1/doctor-details/get-by-id/{doc_id}")
def get_all_doctors(doc_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/doctor-details/get-by-id/{doc_id}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return DoctorController().doctor_details_by_docId(doc_id=doc_id)
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
@doctor_router.post("/v1/doctor-details/addExternal")
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
            return DoctorController().create_doctor(request=request)
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
