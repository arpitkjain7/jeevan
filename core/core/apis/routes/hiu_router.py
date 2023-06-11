from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.hiu_request import RaiseConsent
from core.controllers.hiu_controller import HIUController
from core import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
hiu_router = APIRouter()


@hiu_router.post("/v1/HIU/consentInit")
def raiseConsentRequest(hiu_request: RaiseConsent, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/HIU/consentInit endpoint")
        logging.debug(f"Request: {hiu_request}")
        logging.debug(f"{hiu_request.purpose}")
        request = hiu_request.dict()
        logging.info(f"{request=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            return HIUController().raise_consent(request=hiu_request)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(f"Error in /v1/HIU/consentInit endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HIU/consentInit endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hiu_router.post("/v0.5/consent-requests/on-init")
def raiseConsentRequest(consent_init_request: dict):
    try:
        logging.info("Calling /v0.5/consent-requests/on-init endpoint")
        logging.debug(f"Request: {consent_init_request}")
        return HIUController().consent_on_init(request=consent_init_request)
    except HTTPException as httperror:
        logging.error(f"Error in /v0.5/consent-requests/on-init endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v0.5/consent-requests/on-init endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


# need to work after PHR app is up
@hiu_router.post("/v0.5/consents/hiu/notify")
def consentNotifyHIU(consent_notify: dict):
    try:
        logging.info("Calling /v0.5/consents/hiu/notify endpoint")
        logging.info(f"Notify Request: {consent_notify=}")
    except HTTPException as httperror:
        logging.error(f"Error in /v0.5/consents/hiu/notify endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v0.5/consents/hiu/notify endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
