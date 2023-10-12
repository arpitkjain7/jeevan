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
