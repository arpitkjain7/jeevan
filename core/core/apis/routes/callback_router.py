from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.controllers.callback_controller import CallbackController
from core import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
callback_router = APIRouter()


@callback_router.post("/v0.5/users/auth/on-fetch-modes")
def on_fetch_modes(fetch_modes_request: dict):
    pass
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
def on_confirm(auth_confirm_request: dict):
    try:
        logging.info("Calling /v0.5/users/auth/on-confirm endpoint")
        logging.debug(f"Request: {auth_confirm_request}")
        return CallbackController().on_auth_confirm(request=auth_confirm_request)
    except Exception as error:
        logging.error(f"Error in /v0.5/users/auth/on-confirm endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
