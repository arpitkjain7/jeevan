from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.ondcFS_request import OnSubscribe
from core.controllers.ondcFs_controller import OndcFsController
from commons.auth import decodeJWT
from fastapi.security import OAuth2PasswordRequestForm
from core import logger

logging = logger(__name__)
ondcFs_router = APIRouter()


@ondcFs_router.post("/v1/on_subscribe")
def on_subscribe(on_subscribe_request: OnSubscribe):
    try:
        logging.info("Calling /v1/on_subscribe endpoint")
        logging.debug(f"Request: {on_subscribe_request}")
        return OndcFsController().on_subscribe_decypt(request=on_subscribe_request)
    except Exception as error:
        logging.error(f"Error in /v1/on_subscribe endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
