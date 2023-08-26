from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from gateway.controllers.context_callback_controller import ContextCallbackController
from gateway import logger
from commons.auth import decodeJWT
from datetime import datetime, timezone

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
patient_context_router = APIRouter()


# Patien Context flow
@patient_context_router.post("/v0.5/links/link/on-add-contexts")
async def on_add_context(auth_confirm_request: Request):
    try:
        logging.info("Calling /v0.5/links/link/on-add-contexts endpoint")
        request_dict = await auth_confirm_request.json()
        logging.debug(f"Request: {request_dict}")
        hip_id = auth_confirm_request.headers.get("X-HIP-ID")
        logging.debug(f"hip_id: {hip_id}")
        return ContextCallbackController().on_add_context(
            request=request_dict, hip_id=hip_id
        )
    except Exception as error:
        logging.error(f"Error in /v0.5/links/link/on-add-contexts endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


# Patient Context flow
@patient_context_router.post("/v0.5/links/context/on-notify")
async def on_add_context(auth_confirm_request: Request):
    try:
        logging.info("Calling /v0.5/links/context/on-notify endpoint")
        request_dict = await auth_confirm_request.json()
        logging.debug(f"Request: {request_dict}")
        hip_id = auth_confirm_request.headers.get("X-HIP-ID")
        logging.debug(f"hip_id: {hip_id}")
        return ContextCallbackController().on_add_context(
            request=request_dict, hip_id=hip_id
        )
    except Exception as error:
        logging.error(f"Error in /v0.5/links/context/on-notify endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
