from fastapi import APIRouter, HTTPException, status, Depends, UploadFile
from fastapi.security import OAuth2PasswordBearer
from core.controllers.ai_controller import AIController
from core.apis.schemas.requests.ai_request import MedicalSummary
from core import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
ai_router = APIRouter()


@ai_router.post("/v1/openAI/transcribe")
async def transcribe_audio(
    pmr_id: str,
    patient_id: str,
    audio_file: UploadFile,
    regenerate: bool = False,
    translate: bool = True,
    token: str = Depends(oauth2_scheme),
):
    try:
        logging.info("Calling /v1/openAI/transcribe endpoint")
        logging.debug(f"Request: {patient_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            audio_file_data = await audio_file.read()
            audio_file_name = audio_file.filename
            return AIController().whisper_transcribe(
                patient_id=patient_id,
                pmr_id=pmr_id,
                audio_file_data=audio_file_data,
                audio_file_name=audio_file_name,
                translate=translate,
                regenerate=regenerate,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/openAI/transcribe endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/openAI/transcribe endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@ai_router.post("/v1/openAI/update-summary")
async def update_summary(
    request: MedicalSummary,
    token: str = Depends(oauth2_scheme),
):
    try:
        logging.info("Calling /v1/openAI/update-summary endpoint")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return AIController().update_summary(request=request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/openAI/update-summary endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/openAI/update-summary endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
