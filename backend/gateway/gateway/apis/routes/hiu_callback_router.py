from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from gateway.controllers.hiu_callback_controller import HIUCallbackController
from gateway import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
hiu_callback_router = APIRouter()


@hiu_callback_router.post("/v0.5/consent-requests/on-init")
def raiseConsentRequest(consent_init_request: dict):
    try:
        logging.info("Calling /v0.5/consent-requests/on-init endpoint")
        logging.debug(f"Request: {consent_init_request}")
        return HIUCallbackController().consent_on_init(request=consent_init_request)
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


@hiu_callback_router.post("/v0.5/consents/hiu/notify")
def consentNotifyHIU(consent_notify: dict):
    try:
        logging.info("Calling /v0.5/consents/hiu/notify endpoint")
        logging.info(f"Notify Request: {consent_notify=}")
        return HIUCallbackController().hiu_notify(request=consent_notify)
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


@hiu_callback_router.post("/v0.5/patients/on-find")
def patientOnFind(patient_data: dict):
    try:
        logging.info("Calling /v0.5/patients/on-find endpoint")
        logging.info(f"patientOnFind Request: {patient_data=}")
        return HIUCallbackController().on_find_patient(request=patient_data)
    except HTTPException as httperror:
        logging.error(f"Error in /v0.5/patients/on-find endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v0.5/patients/on-find endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hiu_callback_router.post("/v0.5/consents/on-fetch")
def consentOnFetch(consent_on_fetch: dict):
    try:
        logging.info("Calling /v0.5/consents/on-fetch endpoint")
        logging.info(f"Request: {consent_on_fetch=}")
        return HIUCallbackController().hiu_fetch_consent(request=consent_on_fetch)
    except HTTPException as httperror:
        logging.error(f"Error in /v0.5/consents/on-fetch endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v0.5/consents/on-fetch endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hiu_callback_router.post("/v1/HIU/receiveData")
def receive_data(receive_data: dict):
    try:
        logging.info("Calling /v1/HIU/receiveData endpoint")
        logging.info(f"Request: {receive_data=}")
        return HIUCallbackController().hiu_process_patient_data(request=receive_data)
    except HTTPException as httperror:
        logging.error(f"Error in /v1/HIU/receiveData endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HIU/receiveData endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hiu_callback_router.post("/v0.5/health-information/hiu/on-request")
def healthInfoOnRequest(receive_data: dict):
    try:
        logging.info("Calling /v0.5/health-information/hiu/on-request endpoint")
        logging.info(f"Request: {receive_data=}")
        return HIUCallbackController().health_info_hiu_on_request(request=receive_data)
    except HTTPException as httperror:
        logging.error(
            f"Error in /v0.5/health-information/hiu/on-request endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(
            f"Error in /v0.5/health-information/hiu/on-request endpoint: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
