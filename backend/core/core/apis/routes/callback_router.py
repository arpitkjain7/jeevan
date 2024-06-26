from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from core.controllers.callback_controller import CallbackController
from core import logger
from commons.auth import decodeJWT
from datetime import datetime, timezone

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
callback_router = APIRouter()


@callback_router.post("/v0.5/users/auth/on-fetch-modes")
def on_fetch_modes(fetch_modes_request: dict):
    try:
        logging.info("Calling /v0.5/users/auth/on-fetch-modes endpoint")
        logging.debug(f"Request: {fetch_modes_request}")
        return CallbackController().on_fetch_modes(request=fetch_modes_request)
    except Exception as error:
        logging.error(f"Error in /v0.5/users/auth/on-fetch-modes endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@callback_router.post("/v0.5/users/auth/on-init")
def on_init(auth_init_request: dict):
    try:
        logging.info("Calling /v0.5/users/auth/on-init endpoint")
        logging.debug(f"Request: {auth_init_request}")
        return CallbackController().on_auth_init(request=auth_init_request)
    except Exception as error:
        logging.error(f"Error in /v0.5/users/auth/on-init endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@callback_router.post("/v0.5/users/auth/on-confirm")
async def on_confirm(auth_confirm_request: Request):
    try:
        logging.info("Calling /v0.5/users/auth/on-confirm endpoint")
        request_dict = await auth_confirm_request.json()
        logging.debug(f"Request: {request_dict}")
        hip_id = auth_confirm_request.headers.get("X-HIP-ID")
        logging.debug(f"hip_id: {hip_id}")
        return CallbackController().on_auth_confirm(request=request_dict, hip_id=hip_id)
    except Exception as error:
        logging.error(f"Error in /v0.5/users/auth/on-confirm endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@callback_router.post("/v0.5/links/link/on-add-contexts")
async def on_add_context(auth_confirm_request: Request):
    try:
        logging.info("Calling /v0.5/links/link/on-add-contexts endpoint")
        request_dict = await auth_confirm_request.json()
        logging.debug(f"Request: {request_dict}")
        hip_id = auth_confirm_request.headers.get("X-HIP-ID")
        logging.debug(f"hip_id: {hip_id}")
        return CallbackController().on_add_context(request=request_dict, hip_id=hip_id)
    except Exception as error:
        logging.error(f"Error in /v0.5/links/link/on-add-contexts endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@callback_router.post("/v0.5/links/context/on-notify")
async def on_add_context(auth_confirm_request: Request):
    try:
        logging.info("Calling /v0.5/links/context/on-notify endpoint")
        request_dict = await auth_confirm_request.json()
        logging.debug(f"Request: {request_dict}")
        hip_id = auth_confirm_request.headers.get("X-HIP-ID")
        logging.debug(f"hip_id: {hip_id}")
        return CallbackController().on_add_context(request=request_dict, hip_id=hip_id)
    except Exception as error:
        logging.error(f"Error in /v0.5/links/context/on-notify endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@callback_router.post("/v0.5/patients/status/on-notify")
async def on_status_notify(auth_confirm_request: Request):
    try:
        logging.info("Calling /v0.5/patients/status/on-notify endpoint")
        request_dict = await auth_confirm_request.json()
        logging.debug(f"Request: {request_dict}")
        # hip_id = auth_confirm_request.headers.get("X-HIP-ID")
        # logging.debug(f"hip_id: {hip_id}")
        # return CallbackController().on_add_context(request=request_dict, hip_id=hip_id)
    except Exception as error:
        logging.error(f"Error in /v0.5/patients/status/on-notify endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@callback_router.get("/v0.5/heartbeat")
def heartbeat():
    try:
        logging.info("Calling /v0.5/heartbeat endpoint")
        return {
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f"),
            "status": "UP",
        }
    except Exception as error:
        logging.error(f"Error in /v0.5/heartbeat endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
