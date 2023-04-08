from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends,
    Form,
    UploadFile,
    BackgroundTasks,
)
from typing import List
from fastapi.security import OAuth2PasswordBearer
from core.controllers.annotations_controller import AnnotationController
from commons.auth import decodeJWT
from core import logger

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
annotation_router = APIRouter()


@annotation_router.post("/v1/annotation/selfiUpload")
async def upload_selfi(file: UploadFile, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/annotation/selfiUpload endpoint")
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
            return AnnotationController().add_user_selfi(
                user_id=user_id,
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
        logging.error(f"Error in /v1/annotation/selfiUpload endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/annotation/selfiUpload endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@annotation_router.post("/v1/annotation/start/{event_id}")
async def start_annotation(
    event_id: str, bg_task: BackgroundTasks, token: str = Depends(oauth2_scheme)
):
    try:
        logging.info(f"Calling /v1/annotation/start/{event_id} endpoint")
        logging.debug(f"Request: {event_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            user_id = authenticated_user_details.get("email_id")
            if AnnotationController().check_event_validity(
                user_id=user_id, event_id=event_id
            ):
                if AnnotationController().check_user_validity(user_id=user_id):
                    bg_task.add_task(
                        AnnotationController().start_annotation, event_id, user_id
                    )
                    return {"status": "SUCCESS", "message": "Image Annotation Started"}
                else:
                    raise HTTPException(
                        status_code=status.HTTP_406_NOT_ACCEPTABLE,
                        detail="User selfi not found",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail="Event or User not activated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/annotation/start/{event_id} endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/annotation/start/{event_id} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
