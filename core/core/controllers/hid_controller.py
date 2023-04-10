from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from fastapi import APIRouter, HTTPException, status, Depends
from core import logger
from core.utils.custom.external_call import APIInterface
from core.utils.custom.session_helper import get_session_token
from datetime import datetime, timezone
import os
import uuid

logging = logger(__name__)


class HIDController:
    def __init__(self):
        self.CRUDGatewayInteraction = CRUDGatewayInteraction()
        self.abha_url = os.environ["abha_url"]

    def aadhaar_generateOTP(self, aadhaar_number: str):
        """[Controller to fetch patient auth modes]

        Args:
            request ([dict]): [fetch auth modes request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing  aadhaar_generateOTP function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            generate_aadhaar_otp_url = (
                f"{self.abha_url}/v1/registration/aadhaar/generateOtp"
            )
            resp, resp_code = APIInterface().post(
                route=generate_aadhaar_otp_url,
                data={"aadhaar": aadhaar_number},
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            txn_id = resp.get("txnId")
            if resp_code <= 250:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "AADHAAR_OTP_GENERATION",
                    "request_status": "INIT",
                }
                self.CRUDGatewayInteraction.create(**gateway_request)
                return gateway_request
            else:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "AADHAAR_OTP_GENERATION",
                    "request_status": "FAILED",
                    "error_message": resp.get("details")[0].get("message"),
                    "error_code": resp.get("details")[0].get("code"),
                }
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=gateway_request,
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except Exception as error:
            logging.error(
                f"Error in HIDController.aadhaar_generateOTP function: {error}"
            )
            raise error

    def aadhaar_verifyOTP(self, otp: str, txn_id: str):
        """[Controller to fetch patient auth modes]

        Args:
            request ([dict]): [fetch auth modes request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing  aadhaar_verifyOTP function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            generate_aadhaar_otp_url = (
                f"{self.abha_url}/v1/registration/aadhaar/verifyOTP"
            )
            resp, resp_code = APIInterface().post(
                route=generate_aadhaar_otp_url,
                data={"otp": otp, "txnId": txn_id},
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            if resp_code <= 250:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "OTP_VERIFICATION",
                    "request_status": "IN-PROGRESS",
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
                return gateway_request
            else:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "OTP_VERIFICATION",
                    "request_status": "FAILED",
                    "error_message": resp.get("details")[0].get("message"),
                    "error_code": resp.get("details")[0].get("code"),
                }
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=gateway_request,
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except Exception as error:
            logging.error(f"Error in HIDController.aadhaar_verifyOTP function: {error}")
            raise error

    def aadhaar_generateMobileOTP(self, mobile_number: str, txn_id: str):
        """[Controller to fetch patient auth modes]

        Args:
            request ([dict]): [fetch auth modes request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing  aadhaar_generateMobileOTP function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            generate_aadhaar_otp_url = (
                f"{self.abha_url}/v1/registration/aadhaar/generateMobileOTP"
            )
            resp, resp_code = APIInterface().post(
                route=generate_aadhaar_otp_url,
                data={"mobile": mobile_number, "txnId": txn_id},
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            if resp_code <= 250:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "MOBILE_OTP_GENERATION",
                    "request_status": "IN-PROGRESS",
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
                return gateway_request
            else:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "MOBILE_OTP_GENERATION",
                    "request_status": "FAILED",
                    "error_message": resp.get("details")[0].get("message"),
                    "error_code": resp.get("details")[0].get("code"),
                }
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=gateway_request,
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except Exception as error:
            logging.error(
                f"Error in HIDController.aadhaar_generateMobileOTP function: {error}"
            )
            raise error

    def aadhaar_verifyMobileOTP(self, otp: str, txn_id: str):
        """[Controller to fetch patient auth modes]

        Args:
            request ([dict]): [fetch auth modes request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing  aadhaar_verifyMobileOTP function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            generate_aadhaar_otp_url = (
                f"{self.abha_url}/v1/registration/aadhaar/verifyMobileOTP"
            )
            resp, resp_code = APIInterface().post(
                route=generate_aadhaar_otp_url,
                data={"otp": otp, "txnId": txn_id},
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            if resp_code <= 250:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "MOBILE_OTP_VERIFICATION",
                    "request_status": "IN-PROGRESS",
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
                return gateway_request
            else:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "MOBILE_OTP_VERIFICATION",
                    "request_status": "FAILED",
                    "error_message": resp.get("details")[0].get("message"),
                    "error_code": resp.get("details")[0].get("code"),
                }
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=gateway_request,
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except Exception as error:
            logging.error(
                f"Error in HIDController.aadhaar_verifyMobileOTP function: {error}"
            )
            raise error

    def aadhaar_registration(self, request):
        """[Controller to fetch patient auth modes]

        Args:
            request ([dict]): [fetch auth modes request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing  aadhaar_registration function")
            request_json = request.dict()
            txn_id = request_json.get("txnId")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            generate_aadhaar_otp_url = (
                f"{self.abha_url}/v1/registration/aadhaar/createHealthIdWithPreVerified"
            )
            resp, resp_code = APIInterface().post(
                route=generate_aadhaar_otp_url,
                data=request_json,
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            if resp_code <= 250:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "ABHA_ID_GENERATION",
                    "request_status": "SUCCESS",
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
                return resp
            else:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "ABHA_ID_GENERATION",
                    "request_status": "FAILED",
                    "error_message": resp.get("details")[0].get("message"),
                    "error_code": resp.get("details")[0].get("code"),
                }
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=gateway_request,
                    headers={"WWW-Authenticate": "Bearer"},
                )

        except Exception as error:
            logging.error(
                f"Error in HIDController.aadhaar_verifyMobileOTP function: {error}"
            )
            raise error
