from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends,
    UploadFile,
    BackgroundTasks,
)
from typing import List
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.event_request import CreateEvent, AddImageUrl
from core.apis.schemas.responses.event_response import CreateEventResponse
from core.controllers.event_management_controller import EventManagementController
from commons.auth import decodeJWT
from core import logger

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
event_router = APIRouter()


@event_router.post("/v1/event/create", response_model=CreateEventResponse)
def create_event(
    create_event_request: CreateEvent, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/event/create endpoint")
        logging.debug(f"Request: {create_event_request}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            user_id = authenticated_user_details["email_id"]
            logging.debug(f"{authenticated_user_details=}")
            logging.debug(f"{user_id=}")
            event_obj = EventManagementController().create_event_controller(
                create_event_request, owner_id=user_id
            )
            return CreateEventResponse(**event_obj)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/event/create endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/event/create endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@event_router.get("/v1/event/readByUser/{user_id}")
def get_event_by_user(user_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/event/readByUser/{user_id} endpoint")
        logging.debug(f"Request: {user_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            event_obj = EventManagementController().get_event_by_user_controller(
                user_id=user_id
            )
            return event_obj
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/event/readByUser/{user_id} endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/event/readByUser/{user_id} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error,
            headers={"WWW-Authenticate": "Bearer"},
        )


@event_router.get("/v1/event/readByEvent/{event_id}")
def get_event(event_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/event/readByEvent/{event_id} endpoint")
        logging.debug(f"Request: {event_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            event_obj = EventManagementController().get_event_controller(
                event_id=event_id
            )
            return event_obj
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/event/readByEvent/{event_id} endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/event/readByEvent/{event_id} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error,
            headers={"WWW-Authenticate": "Bearer"},
        )


@event_router.get("/v1/event/readByEventUUID/{event_uuid}")
def get_event_by_uuid(event_uuid: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/event/readByEventUUID/{event_uuid} endpoint")
        logging.debug(f"Request: {event_uuid=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return EventManagementController().get_event_by_uuid_controller(
                event_uuid=event_uuid
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/event/readByEventUUID/{event_uuid} endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(
            f"Error in /v1/event/readByEventUUID/{event_uuid} endpoint: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error,
            headers={"WWW-Authenticate": "Bearer"},
        )


@event_router.get("/v1/event/getEventMetadata/{event_uuid}")
def get_event_metadata_by_uuid(event_uuid: str):
    try:
        logging.info(f"Calling /v1/event/getEventMetadata/{event_uuid} endpoint")
        logging.debug(f"Request: {event_uuid=}")
        return EventManagementController().get_event_metadata_by_uuid_controller(
            event_uuid=event_uuid
        )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/event/readByEventUUID/{event_uuid} endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(
            f"Error in /v1/event/readByEventUUID/{event_uuid} endpoint: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error,
            headers={"WWW-Authenticate": "Bearer"},
        )


@event_router.get("/v1/event/getQR/{event_id}")
def get_QR(event_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/event/getQR/{event_id} endpoint")
        logging.debug(f"Request: {event_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return EventManagementController().get_qr_controller(event_id=event_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/event/getQR/{event_id} endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/event/getQR/{event_id} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error,
            headers={"WWW-Authenticate": "Bearer"},
        )


@event_router.post("/v1/event/uploadImage/{event_id}")
async def addImages(
    event_id: str,
    bg_task: BackgroundTasks,
    files: List[UploadFile],
    token: str = Depends(oauth2_scheme),
):
    try:
        logging.info(f"Calling /v1/event/uploadImage/{event_id} endpoint")
        logging.debug(f"Request: {event_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            user_id = authenticated_user_details.get("email_id")
            for _, file in enumerate(files):
                file_type = file.content_type
                if file_type not in ["image/jpeg", "image/png"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"{file_type} is not allowed in the request. Try using image/jpeg or image/png",
                    )
                contents = await file.read()
                bg_task.add_task(
                    EventManagementController().add_image_controller,
                    user_id,
                    event_id,
                    contents,
                    file.filename,
                )
            return {"status": "Upload started"}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/event/uploadImage/{event_id} endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/event/uploadImage/{event_id} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@event_router.post("/v1/event/addCoverPhoto/{event_id}")
async def add_cover_photo(
    event_id: str, file: UploadFile, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info("Calling /v1/event/addCoverPhoto endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            user_id = authenticated_user_details.get("email_id")
            file_type = file.content_type
            if file_type not in ["image/jpeg", "image/png"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{file_type} is not allowed in the request. Try using image/jpeg or image/png",
                )
            contents = await file.read()
            return EventManagementController().add_cover_photo(
                user_id=user_id,
                event_id=event_id,
                data=contents,
                file_name=file.filename,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/event/addCoverPhoto endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/event/addCoverPhoto endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@event_router.post("/v1/event/authenticate/{event_uuid}")
async def authenticateEvent(
    event_uuid: str, pass_code: str, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info(f"Calling /v1/event/authenticate/{event_uuid} endpoint")
        logging.debug(f"Request: {event_uuid=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            user_id = authenticated_user_details.get("email_id")
            return EventManagementController().activate_event_controller(
                event_uuid=event_uuid, user_id=user_id, pass_code=pass_code
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/event/authenticate/{event_uuid} endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/event/authenticate/{event_uuid} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@event_router.post("/v1/event/publish/{event_id}")
async def publishEvent(
    event_id: str, event_status: str, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info(f"Calling /v1/event/publish/{event_id} endpoint")
        logging.debug(f"Request: {event_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            user_id = authenticated_user_details.get("email_id")
            return EventManagementController().publish_event_controller(
                event_id=event_id, event_status=event_status
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/event/publish/{event_id} endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/event/publish/{event_id} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@event_router.get("/v1/event/listImages/{event_id}")
async def getEventImages(event_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/event/listImages/{event_id} endpoint")
        logging.debug(f"Request: {event_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            user_id = authenticated_user_details.get("email_id")
            return EventManagementController().get_event_images_controller(
                event_id=event_id, user_id=user_id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/event/listImages/{event_id} endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/event/listImages/{event_id} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@event_router.get("/v1/event/listImagesToApprove/{event_id}")
async def getImagesToApprove(event_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/event/listImagesToApprove/{event_id} endpoint")
        logging.debug(f"Request: {event_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            user_id = authenticated_user_details.get("email_id")
            return EventManagementController().get_event_images_for_approval_controller(
                event_id=event_id, user_id=user_id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/event/listImagesToApprove/{event_id} endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(
            f"Error in /v1/event/listImagesToApprove/{event_id} endpoint: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@event_router.delete("/v1/event/deleteImage/{image_id}")
async def deleteImage(image_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/event/deleteImage/{image_id} endpoint")
        logging.debug(f"Request: {image_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            user_id = authenticated_user_details.get("email_id")
            return EventManagementController().delete_image(image_id=image_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/event/deleteImage/{image_id} endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/event/deleteImage/{image_id} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@event_router.post("/v1/event/approveImage/{image_id}")
async def approveImage(image_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/event/approveImage/{image_id} endpoint")
        logging.debug(f"Request: {image_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            user_id = authenticated_user_details.get("email_id")
            return EventManagementController().approve_image(image_id=image_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/event/approveImage/{image_id} endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/event/approveImage/{image_id} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@event_router.post("/v1/event/approveAllImages")
async def approveAllImages(
    event_id: str, owner_id: str, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info(f"Calling /v1/event/approveAllImages endpoint")
        logging.debug(f"Request: {event_id=}")
        logging.debug(f"Request: {owner_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            user_id = authenticated_user_details.get("email_id")
            return EventManagementController().approve_all_images(
                event_id=event_id, owner_id=owner_id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/event/approveAllImages endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/event/approveAllImages endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@event_router.post("/v2/event/uploadImage/{event_id}")
async def addImageUrls(
    event_id: str,
    bg_task: BackgroundTasks,
    files: AddImageUrl,
    token: str = Depends(oauth2_scheme),
):
    try:
        logging.info(f"Calling /v2/event/uploadImage/{event_id} endpoint")
        logging.debug(f"Request: {event_id=}")
        logging.debug(f"Request: {files=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            user_id = authenticated_user_details["email_id"]
            bg_task.add_task(
                EventManagementController().add_image_urls_controller,
                event_id,
                files,
                user_id,
            )
            return {"status": "Upload started"}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v2/event/uploadImage/{event_id} endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v2/event/uploadImage/{event_id} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@event_router.get("/v1/event/validityStatus/{event_uuid}")
async def getValidityStatus(event_uuid: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/event/validityStatus/{event_uuid} endpoint")
        logging.debug(f"Request: {event_uuid=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            user_id = authenticated_user_details.get("email_id")
            return EventManagementController().get_validity_status(
                event_uuid=event_uuid, user_id=user_id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/event/validityStatus/{event_uuid} endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(
            f"Error in /v1/event/validityStatus/{event_uuid} endpoint: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
