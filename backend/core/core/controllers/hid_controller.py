from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from core.crud.hims_patientDetails_crud import CRUDPatientDetails
from fastapi import APIRouter, HTTPException, status, Depends
from core import logger
from core.utils.custom.external_call import APIInterface
from core.utils.custom.session_helper import get_session_token
from datetime import datetime, timezone, timedelta
from core.utils.aws.s3_helper import upload_to_s3, get_object, create_presigned_url
from core.utils.custom.encryption_helper import rsa_encryption
import os
import json
import uuid, pytz

logging = logger(__name__)


class HIDController:
    def __init__(self):
        self.CRUDGatewayInteraction = CRUDGatewayInteraction()
        self.CRUDPatientDetails = CRUDPatientDetails()
        self.abha_url = os.environ["abha_url"]
        self.s3_location = os.environ["s3_location"]

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
            if resp_code <= 250:
                txn_id = resp.get("txnId")
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "AADHAAR_OTP_GENERATION",
                    "request_status": "INIT",
                }
                self.CRUDGatewayInteraction.create(**gateway_request)
                gateway_request.update({"txn_id": txn_id})
                return gateway_request
            else:
                gateway_request = {
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
                    "request_id": str(uuid.uuid1()),
                    "request_type": "OTP_VERIFICATION",
                    "request_status": "IN-PROGRESS",
                    "transaction_id": txn_id,
                }
                self.CRUDGatewayInteraction.create(**gateway_request)
                return gateway_request
            else:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "OTP_VERIFICATION",
                    "request_status": "FAILED",
                    "error_message": resp.get("details")[0].get("message"),
                    "error_code": resp.get("details")[0].get("code"),
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
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
                f"{self.abha_url}/v2/registration/aadhaar/checkAndGenerateMobileOTP"
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
                gateway_request.update(
                    {"txn_id": txn_id, "mobileLinked": resp.get("mobileLinked", False)}
                )
                return gateway_request
            else:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "MOBILE_OTP_GENERATION",
                    "request_status": "FAILED",
                    "error_message": resp.get("details")[0].get("message"),
                    "error_code": resp.get("details")[0].get("code"),
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
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
                gateway_request.update({"txn_id": txn_id})
                return gateway_request
            else:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "MOBILE_OTP_VERIFICATION",
                    "request_status": "FAILED",
                    "error_message": resp.get("details")[0].get("message"),
                    "error_code": resp.get("details")[0].get("code"),
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
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
            logging.info(f"{resp=}")
            logging.info(f"{resp_code=}")
            if resp_code <= 250:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "ABHA_ID_GENERATION",
                    "request_status": "SUCCESS",
                    "callback_response": resp,
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
                linking_token = resp.get("token")
                refresh_token = resp.get("refreshToken")
                logging.info("Getting patient details")
                get_profile_url = f"{self.abha_url}/v1/account/profile"
                patient_data, resp_code = APIInterface().get(
                    route=get_profile_url,
                    headers={
                        "Authorization": f"Bearer {gateway_access_token}",
                        "X-Token": f"Bearer {linking_token}",
                    },
                )
                abha_number = patient_data["healthIdNumber"].replace("-", "")
                patient_id = f"C360-PID-{str(uuid.uuid1().int)[:18]}"
                time_now = datetime.now()
                token_validity = time_now + timedelta(minutes=1440)
                token_validity = token_validity.strftime("%m/%d/%Y, %H:%M:%S")
                patient_request = {
                    "id": patient_id,
                    "abha_number": abha_number,
                    "abha_address": patient_data["healthId"],
                    "mobile_number": patient_data["mobile"],
                    "name": patient_data["name"],
                    "gender": patient_data["gender"],
                    "DOB": f"{patient_data['dayOfBirth']}/{patient_data['monthOfBirth']}/{patient_data['yearOfBirth']}",
                    "email": patient_data["email"],
                    "address": patient_data["address"],
                    "village": patient_data["villageName"],
                    "village_code": patient_data["villageCode"],
                    "town": patient_data["townName"],
                    "town_code": patient_data["townCode"],
                    "district": patient_data["districtName"],
                    "district_code": patient_data["districtCode"],
                    "pincode": patient_data["pincode"],
                    "state_name": patient_data["stateName"],
                    "state_code": patient_data["stateCode"],
                    "hip_id": request_json["hip_id"],
                    "auth_methods": {"authMethods": patient_data["authMethods"]},
                    "linking_token": {
                        "value": linking_token,
                        "valid_till": token_validity,
                    },
                    "refresh_token": {
                        "value": refresh_token,
                        "valid_till": token_validity,
                    },
                    "abha_status": "ACTIVE",
                }
                patient_record = self.CRUDPatientDetails.read_by_abhaId(
                    abha_number=abha_number
                )
                if patient_record:
                    patient_request.update({"id": patient_record["id"]})
                    self.CRUDPatientDetails.update(**patient_request)
                else:
                    self.CRUDPatientDetails.create(**patient_request)
                return patient_request
            else:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "ABHA_ID_GENERATION",
                    "request_status": "FAILED",
                    "error_message": resp.get("details")[0].get("message"),
                    "error_code": resp.get("details")[0].get("code"),
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
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

    def forgot_generateOtp(self, aadhaar_number: str):
        """Generate Aadhaar OTP for getting Abha id from Aadhaar

        Args:
            aadhaar_number (str): Aadhaar Number of patient

        Raises:
            HTTPException: _description_
            error: _description_

        Returns:
            _type_: _description_
        """
        try:
            logging.info("executing  forgot_generateOtp function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            generate_otp_abha_url = (
                f"{self.abha_url}/v1/forgot/healthId/aadhaar/generateOtp"
            )
            resp, resp_code = APIInterface().post(
                route=generate_otp_abha_url,
                data={"aadhaar": aadhaar_number},
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            if resp_code <= 250:
                txn_id = resp.get("txnId")
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "FORGOT_ABHA",
                    "request_status": "INIT",
                }
                self.CRUDGatewayInteraction.create(**gateway_request)
                gateway_request.update({"txn_id": txn_id})
                return gateway_request
            else:
                gateway_request = {
                    "request_type": "FORGOT_ABHA",
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
            logging.error(f"Error in HIDController.abha_verification function: {error}")
            raise error

    def forgot_verifyOtp(self, otp: str, txn_id: str):
        """Verify Aadhaar OTP for getting Abha id from Aadhaar

        Args:
            otp (str): Aadhaar OPT sent to patient
            txn_id (str): Transaction id from previous step

        Raises:
            HTTPException: _description_
            error: _description_

        Returns:
            _type_: _description_
        """
        try:
            logging.info("executing  forgot_generateOtp function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            verify_otp_abha_url = f"{self.abha_url}/v1/forgot/healthId/aadhaar"
            resp, resp_code = APIInterface().post(
                route=verify_otp_abha_url,
                data={"otp": otp, "txnId": txn_id},
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            if resp_code <= 250:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "FORGOT_ABHA",
                    "request_status": "SUCCESS",
                    "callback_response": resp,
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
                return {
                    "health_address": resp.get("healthId"),
                    "health_id": resp.get("healthIdNumber"),
                }
            else:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "FORGOT_ABHA",
                    "request_status": "FAILED",
                    "error_message": resp.get("details")[0].get("message"),
                    "error_code": resp.get("details")[0].get("code"),
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=gateway_request,
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except Exception as error:
            logging.error(f"Error in HIDController.abha_verification function: {error}")
            raise error

    def generateMobileOTP(self, mobile_number: str):
        """[Controller to fetch patient auth modes]

        Args:
            request ([dict]): [fetch auth modes request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing generateMobileOTP function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            generate_mobile_otp_url = (
                f"{self.abha_url}/v1/registration/mobile/generateOtp"
            )
            resp, resp_code = APIInterface().post(
                route=generate_mobile_otp_url,
                data={"mobile": mobile_number},
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            if resp_code <= 250:
                txn_id = resp.get("txnId")
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "MOBILE_OTP_GENERATION",
                    "request_status": "INIT",
                }
                self.CRUDGatewayInteraction.create(**gateway_request)
                gateway_request.update({"txn_id": txn_id})
                return gateway_request
            else:
                gateway_request = {
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
            logging.error(f"Error in HIDController.generateMobileOTP function: {error}")
            raise error

    def verifyMobileOTP(self, otp: str, txn_id: str):
        """[Controller to fetch patient auth modes]

        Args:
            request ([dict]): [fetch auth modes request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing  verifyMobileOTP function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            generate_mobile_otp_url = (
                f"{self.abha_url}/v1/registration/mobile/verifyOtp"
            )
            resp, resp_code = APIInterface().post(
                route=generate_mobile_otp_url,
                data={"otp": otp, "txnId": txn_id},
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            if resp_code <= 250:
                token = resp.get("token")
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "MOBILE_OTP_VERIFICATION",
                    "request_status": "IN-PROGRESS",
                    "token": token,
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
                gateway_request.update({"txn_id": txn_id})
                return gateway_request
            else:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "MOBILE_OTP_VERIFICATION",
                    "request_status": "FAILED",
                    "error_message": resp.get("details")[0].get("message"),
                    "error_code": resp.get("details")[0].get("code"),
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=gateway_request,
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except Exception as error:
            logging.error(f"Error in HIDController.verifyMobileOTP function: {error}")
            raise error

    def mobile_abha_registration(self, request):
        """[Controller to fetch patient auth modes]

        Args:
            request ([dict]): [fetch auth modes request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing  mobile_abha_registration function")
            request_json = request.dict()
            txn_id = request_json.get("txnId")
            dob = request_json.get("dob")
            date, month, year = dob.split("/")
            name = f"{request_json.get('firstName')} {request_json.get('lastName')}"
            token = self.CRUDGatewayInteraction.read(request_id=txn_id).get("token")
            request_json.update(
                {
                    "dayOfBirth": date,
                    "monthOfBirth": str(int(month)),
                    "yearOfBirth": year,
                    "token": token,
                    "name": name,
                }
            )
            request_json.pop("dob")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            generate_mobile_otp_url = (
                f"{self.abha_url}/v1/registration/mobile/createHealthId"
            )
            resp, resp_code = APIInterface().post(
                route=generate_mobile_otp_url,
                data=request_json,
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            logging.info(f"{resp=}")
            logging.info(f"{resp_code=}")
            if resp_code <= 250:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "ABHA_ID_GENERATION",
                    "request_status": "SUCCESS",
                    "callback_response": resp,
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
                time_now = datetime.now()
                token_validity = time_now + timedelta(minutes=1440)
                token_validity = token_validity.strftime("%m/%d/%Y, %H:%M:%S")
                linking_token = resp.get("token")
                refresh_token = resp.get("refreshToken")
                logging.info("Getting patient details")
                patient_id = f"C360-PID-{str(uuid.uuid1().int)[:18]}"
                patient_request = {
                    "id": patient_id,
                    "abha_number": resp["healthIdNumber"],
                    "abha_address": resp["healthId"],
                    "mobile_number": resp["mobile"],
                    "name": name,
                    "gender": resp["gender"],
                    "DOB": dob,
                    "email": resp["email"],
                    "district": resp["districtName"],
                    "district_code": resp["districtCode"],
                    "pincode": resp["pincode"],
                    "state_name": resp["stateName"],
                    "state_code": resp["stateCode"],
                    "auth_methods": {"authMethods": resp["authMethods"]},
                    "hip_id": request_json["hip_id"],
                    "linking_token": {
                        "value": linking_token,
                        "valid_till": token_validity,
                    },
                    "refresh_token": {
                        "value": refresh_token,
                        "valid_till": token_validity,
                    },
                    "abha_status": "ACTIVE",
                }
                patient_record = self.CRUDPatientDetails.read_by_abhaAddress(
                    abha_address=resp["healthId"]
                )
                if patient_record:
                    patient_request.update({"id": patient_record["id"]})
                    self.CRUDPatientDetails.update(**patient_request)
                else:
                    self.CRUDPatientDetails.create(**patient_request)
                return patient_request
            else:
                gateway_request = {
                    "request_id": txn_id,
                    "request_type": "ABHA_ID_GENERATION",
                    "request_status": "FAILED",
                    "error_message": resp.get("details")[0].get("message"),
                    "error_code": resp.get("details")[0].get("code"),
                }
                self.CRUDGatewayInteraction.update(**gateway_request)
                gateway_request.update({"txn_id": txn_id})
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=gateway_request,
                    headers={"WWW-Authenticate": "Bearer"},
                )

        except Exception as error:
            logging.error(
                f"Error in HIDController.mobile_abha_registration function: {error}"
            )
            raise error

    def get_abha_card(self, patient_id: str):
        try:
            logging.info("executing  get_abha_card function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            patient_obj = self.CRUDPatientDetails.read_by_patientId(
                patient_id=patient_id
            )
            logging.info(f"{patient_obj=}")
            if patient_obj:
                logging.info("Getting ABHA S3 location")
                if patient_obj.get("abha_s3_location"):
                    logging.info("Generating Presigned URL for ABHA S3 location")
                    s3_presigned_url = create_presigned_url(
                        bucket_name=self.s3_location,
                        key=patient_obj.get("abha_s3_location"),
                        expires_in=1800,
                    )
                    logging.info("Returning S3 presigned url")
                    return {"abha_url": s3_presigned_url}
                else:
                    logging.info("Getting Abha card")
                    linking_token = patient_obj.get("linking_token").get("value")
                    byte_data, resp_code = APIInterface().get_bytes(
                        route=f"{self.abha_url}/v1/account/getPngCard",
                        headers={
                            "Authorization": f"Bearer {gateway_access_token}",
                            "X-Token": f"Bearer {linking_token}",
                        },
                    )
                    if resp_code >= 400:
                        logging.info(
                            "Expired Linking Token. Generating new with Refresh token"
                        )
                        refresh_token = patient_obj.get("refresh_token").get("value")
                        refresh_token_url = (
                            f"{self.abha_url}/v1/auth/generate/access-token"
                        )
                        resp, resp_code = APIInterface().post(
                            route=refresh_token_url,
                            data={"refreshToken": refresh_token},
                            headers={"Authorization": f"Bearer {gateway_access_token}"},
                        )
                        linking_token = resp.get("accessToken", None)
                        if linking_token:
                            self.CRUDPatientDetails.update(
                                **{
                                    "id": patient_id,
                                    "linking_token": {"value": linking_token},
                                }
                            )
                        logging.info("Getting Abha card")
                        byte_data, resp_code = APIInterface().get_bytes(
                            route=f"{self.abha_url}/v1/account/getPngCard",
                            headers={
                                "Authorization": f"Bearer {gateway_access_token}",
                                "X-Token": f"Bearer {linking_token}",
                            },
                        )
                        logging.info("Uploading Abha card to S3")
                        upload_to_s3(
                            bucket_name=self.s3_location,
                            byte_data=byte_data,
                            content_type="image/png",
                            file_name=f"PATIENT_DATA/{patient_id}/abha.png",
                        )
                        logging.info("Uploading database with S3 location")
                        self.CRUDPatientDetails.update(
                            **{
                                "id": patient_id,
                                "abha_s3_location": f"PATIENT_DATA/{patient_id}/abha.png",
                            }
                        )
                        logging.info("Generating Presigned URL for Abha S3")
                        s3_presigned_url = create_presigned_url(
                            bucket_name=self.s3_location,
                            key=f"PATIENT_DATA/{patient_id}/abha.png",
                            expires_in=1800,
                        )
                        logging.info("Returning S3 presigned url")
                        return {"abha_url": s3_presigned_url}
                    logging.info("Uploading Abha card to S3")
                    upload_to_s3(
                        bucket_name=self.s3_location,
                        byte_data=byte_data,
                        content_type="image/png",
                        file_name=f"PATIENT_DATA/{patient_id}/abha.png",
                    )
                    logging.info("Uploading database with S3 location")
                    self.CRUDPatientDetails.update(
                        **{
                            "id": patient_id,
                            "abha_s3_location": f"PATIENT_DATA/{patient_id}/abha.png",
                        }
                    )
                    logging.info("Generating Presigned URL for Abha S3")
                    s3_presigned_url = create_presigned_url(
                        bucket_name=self.s3_location,
                        key=f"PATIENT_DATA/{patient_id}/abha.png",
                        expires_in=1800,
                    )
                    logging.info("Returning S3 presigned url")
                    return {"abha_url": s3_presigned_url}
        except Exception as error:
            logging.error(
                f"Error in HIDController.mobile_abha_registration function: {error}"
            )
            raise error

    def search_abha(self, abha_number: str):
        try:
            logging.info("executing search_abha function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            search_abha_url = f"{self.abha_url}/v1/search/searchByHealthId"
            resp, resp_code = APIInterface().post(
                route=search_abha_url,
                data={"healthId": abha_number},
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            return resp
        except Exception as error:
            logging.error(f"Error in HIDController.search_abha function: {error}")
            raise error

    def search_mobile(self, mobile_number: str):
        try:
            logging.info("executing search_mobile function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            search_abha_url = f"{self.abha_url}/v1/search/searchByMobile"
            resp, resp_code = APIInterface().post(
                route=search_abha_url,
                data={"mobile": mobile_number},
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            logging.info(f"/v1/search/searchByMobile {resp_code=}")
            if resp.get("healthIdNumber", None):
                return resp
            login_abha_url = f"{self.abha_url}/v2/registration/mobile/login/generateOtp"
            resp, resp_code = APIInterface().post(
                route=login_abha_url,
                data={"mobile": mobile_number},
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            gateway_request = {
                "request_id": resp.get("txnId"),
                "request_type": "ABHA_LOGIN_OTP_GENERATION",
                "request_status": "INIT",
            }
            self.CRUDGatewayInteraction.create(**gateway_request)
            gateway_request.update({"txn_id": resp.get("txnId")})
            return gateway_request
        except Exception as error:
            logging.error(f"Error in HIDController.search_mobile function: {error}")
            raise error

    def verify_login_otp(self, request):
        try:
            logging.info("executing verify_login_otp function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            txn_id = request.txnId
            otp = request.otp
            encrypted_data = rsa_encryption(data_to_encrypt=otp)
            verify_otp_url = f"{self.abha_url}/v2/registration/mobile/login/verifyOtp"
            resp, resp_code = APIInterface().post(
                route=verify_otp_url,
                data={"otp": encrypted_data, "txnId": txn_id},
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            return resp
        except Exception as error:
            logging.error(f"Error in HIDController.verify_login_otp function: {error}")
            raise error

    def abha_auth_init(self, request):
        try:
            logging.info("executing abha_auth_init function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            patient_id = request.patientId
            patient_obj = self.CRUDPatientDetails.read_by_patientId(
                patient_id=patient_id
            )
            health_id = patient_obj.get("abha_number")
            auth_method = request.authMethod
            verify_otp_url = f"{self.abha_url}/v1/auth/init"
            resp, resp_code = APIInterface().post(
                route=verify_otp_url,
                data={"authMethod": auth_method, "healthid": health_id},
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            return resp
        except Exception as error:
            logging.error(f"Error in HIDController.abha_auth_init function: {error}")
            raise error

    def abha_auth_confirm(self, request):
        try:
            logging.info("executing abha_auth_confirm function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            txn_id = request.txnId
            otp = request.otp
            pid = request.patientId
            auth_mode = request.authMode
            if auth_mode == "AADHAAR_OTP":
                verify_otp_url = f"{self.abha_url}/v1/auth/confirmWithAadhaarOtp"
            elif auth_mode == "MOBILE_OTP":
                verify_otp_url = f"{self.abha_url}/v1/auth/confirmWithMobileOTP"
            else:
                return {"status": "failed", "details": "invalid auth mode"}
            resp, resp_code = APIInterface().post(
                route=verify_otp_url,
                data={"otp": otp, "txnId": txn_id},
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            if resp_code <= 250:
                linking_token = resp.get("token")
                refresh_token = resp.get("refreshToken")
                ist_timezone = pytz.timezone("Asia/Kolkata")
                time_now = datetime.now(ist_timezone)
                linking_token_validity = time_now + timedelta(
                    seconds=resp.get("expiresIn")
                )
                linking_token_validity = linking_token_validity.strftime(
                    "%m/%d/%Y, %H:%M:%S"
                )
                refresh_token_validity = time_now + timedelta(
                    seconds=resp.get("refreshExpiresIn")
                )
                refresh_token_validity = refresh_token_validity.strftime(
                    "%m/%d/%Y, %H:%M:%S"
                )
                self.CRUDPatientDetails.update(
                    **{
                        "id": pid,
                        "linking_token": {
                            "value": linking_token,
                            "valid_till": linking_token_validity,
                        },
                        "refresh_token": {
                            "value": refresh_token,
                            "valid_till": refresh_token_validity,
                        },
                    }
                )
            return resp
        except Exception as error:
            logging.error(f"Error in HIDController.abha_auth_confirm function: {error}")
            raise error
