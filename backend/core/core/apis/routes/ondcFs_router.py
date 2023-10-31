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
        ondc_public_key = "MCowBQYDK2VuAyEAduMuZgmtpjdCuxv+Nc49K0cB6tL/Dj3HZetvVN7ZekM="
        enc_private_key = (
            "MC4CAQAwBQYDK2VuBCIEIAixt1l8nWtgbAHV714v09pRXapX6oFi2/uN9Vkp5mFD"
        )
        logging.info(f"{enc_private_key=}")
        return OndcFsController().on_subscribe_decypt(
            ondc_public_key, enc_private_key, request=on_subscribe_request
        )
    except Exception as error:
        logging.error(f"Error in /v1/on_subscribe endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
