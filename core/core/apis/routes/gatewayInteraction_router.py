from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.controllers.gatewayInteraction_controller import GatewayController
from core import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
gateway_router = APIRouter()


@gateway_router.get("/v1/gatewayInteraction/{request_id}")
def get_status(request_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info(f"Calling /v1/gatewayInteraction/{request_id} endpoint")
        logging.debug(f"Request: {request_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return GatewayController().get_status(request_id=request_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/gatewayInteraction/{request_id} endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/gatewayInteraction/{request_id} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
