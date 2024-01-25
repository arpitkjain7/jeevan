from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from core.apis.schemas.requests.hiu_request import RaiseConsent, FindPatient
from core.apis.schemas.responses.hiu_response import Consent, ConsentDetails
from core.controllers.hiu_controller import HIUController
from core import logger
from commons.auth import decodeJWT

logging = logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signIn")
hiu_router = APIRouter()


@hiu_router.get("/v1/HIU/listConsent/{patient_id}", response_model=list[Consent])
def list_all_consent(patient_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/HIU/listConsent/{patient_id} endpoint")
        logging.debug(f"Request: {patient_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            consent_list = HIUController().list_consent(patient_id=patient_id)
            return [Consent(**consent) for consent in consent_list]
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/HIU/listConsent/{patient_id} endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HIU/listConsent/{patient_id} endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hiu_router.get(
    "/v1/HIU/listApprovedConsent/{patient_id}", response_model=list[Consent]
)
def list_approved_consent(patient_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/HIU/listApprovedConsent/{patient_id} endpoint")
        logging.debug(f"Request: {patient_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            consent_list = HIUController().list_approved_consent(patient_id=patient_id)
            return [Consent(**consent) for consent in consent_list]
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/HIU/listApprovedConsent/{patient_id} endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(
            f"Error in /v1/HIU/listApprovedConsent/{patient_id} endpoint: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hiu_router.get("/v1/HIU/getConsentDetails/{consent_id}", response_model=ConsentDetails)
def get_consent_details(consent_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/HIU/getConsentDetails/{consent_id} endpoint")
        logging.debug(f"Request: {consent_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            consent_details = HIUController().get_consent_details(consent_id=consent_id)
            return ConsentDetails(**consent_details)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/HIU/getConsentDetails/{consent_id} endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(
            f"Error in /v1/HIU/getConsentDetails/{consent_id} endpoint: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hiu_router.get("/v1/HIU/getCareContext/{consent_id}")
def get_care_context(consent_id: str, token: str = Depends(oauth2_scheme)):
    try:
        logging.info("Calling /v1/HIU/getCareContext/{consent_id} endpoint")
        logging.debug(f"Request: {consent_id=}")
        authenticated_user_details = decodeJWT(token=token)
        if authenticated_user_details:
            consent_details = HIUController().get_consent_details(consent_id=consent_id)
            return consent_details
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException as httperror:
        logging.error(
            f"Error in /v1/HIU/getCareContext/{consent_id} endpoint: {httperror}"
        )
        raise httperror
    except Exception as error:
        logging.error(
            f"Error in /v1/HIU/getConsentDetails/{consent_id} endpoint: {error}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


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


@hiu_router.post("/v0.5/consents/hiu/notify")
def consentNotifyHIU(consent_notify: dict):
    try:
        logging.info("Calling /v0.5/consents/hiu/notify endpoint")
        logging.info(f"Notify Request: {consent_notify=}")
        return HIUController().hiu_notify(request=consent_notify)
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


@hiu_router.post("/v1/HIU/findPatient")
def patientFind(patient_data: FindPatient):
    try:
        logging.info("Calling /v1/HIU/findPatient endpoint")
        logging.info(f"patientFind Request: {patient_data=}")
        return HIUController().find_patient(request=patient_data)
    except HTTPException as httperror:
        logging.error(f"Error in /v1/HIU/findPatient endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HIU/findPatient endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )


@hiu_router.post("/v0.5/patients/on-find")
def patientOnFind(patient_data: dict):
    try:
        logging.info("Calling /v0.5/patients/on-find endpoint")
        logging.info(f"patientOnFind Request: {patient_data=}")
        return HIUController().on_find_patient(request=patient_data)
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


@hiu_router.post("/v0.5/consents/on-fetch")
def consentOnFetch(consent_on_fetch: dict):
    try:
        logging.info("Calling /v0.5/consents/on-fetch endpoint")
        logging.info(f"Request: {consent_on_fetch=}")
        return HIUController().hiu_fetch_consent(request=consent_on_fetch)
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


@hiu_router.post("/v1/HIU/receiveData")
def receive_data(receive_data: dict):
    try:
        logging.info("Calling /v1/HIU/receiveData endpoint")
        logging.info(f"Request: {receive_data=}")
        return HIUController().hiu_process_patient_data(request=receive_data)
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


@hiu_router.post("/v0.5/health-information/hiu/on-request")
def healthInfoOnRequest(receive_data: dict):
    try:
        logging.info("Calling /v0.5/health-information/hiu/on-request endpoint")
        logging.info(f"Request: {receive_data=}")
        return HIUController().health_info_hiu_on_request(request=receive_data)
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


@hiu_router.post("/v1/HIU/storeData")
def store_processed_data(processed_data: dict):
    try:
        logging.info("Calling /v1/HIU/storeData endpoint")
        logging.info(f"Request: {processed_data=}")
        return HIUController().hiu_store_patient_data(request=processed_data)
    except HTTPException as httperror:
        logging.error(f"Error in /v1/HIU/storeData endpoint: {httperror}")
        raise httperror
    except Exception as error:
        logging.error(f"Error in /v1/HIU/storeData endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
