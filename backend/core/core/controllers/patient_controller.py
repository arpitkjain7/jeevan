from core.crud.hims_patientDetails_crud import CRUDPatientDetails
from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from core.crud.hims_hip_crud import CRUDHIP
from core.crud.hims_patientMedicalRecord_crud import CRUDPatientMedicalRecord
from core.crud.hims_vitals_crud import CRUDVital
from core.utils.custom.external_call import APIInterface
from core.utils.custom.msg91_helper import otpHelper
from core.utils.custom.session_helper import get_session_token
from commons.auth import decodeJWT
from core import logger
from core.utils.custom.fuzzy_match import FuzzyMatch
from datetime import datetime, timezone, timedelta
import os, json
import uuid
from pytz import timezone as pytz_timezone
from core.utils.custom.patient_helper import calculate_age

logging = logger(__name__)


class PatientController:
    def __init__(self):
        self.CRUDPatientDetails = CRUDPatientDetails()
        self.CRUDGatewayInteraction = CRUDGatewayInteraction()
        self.CRUDHIP = CRUDHIP()
        self.CRUDPatientMedicalRecord = CRUDPatientMedicalRecord()
        self.CRUDVital = CRUDVital()
        self.gateway_url = os.environ["gateway_url"]
        self.abha_url = os.environ["abha_url"]
        self.s3_location = os.environ["s3_location"]
        self.msg91_template_id = os.environ["msg91_template_id"]

    def abha_verification(self, health_id: str, year_of_birth: str):
        """Verify if the abha address already exists
        Args:
            health_id (str): abha address to be checked
        Raises:
            HTTPException: _description_
            error: _description_
        Returns:
            _type_: _description_
        """
        try:
            logging.info("executing  abha_verification function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            verify_abha_url = f"{self.abha_url}/v2/search/searchHealthIdToLogin"
            resp, resp_code = APIInterface().post(
                route=verify_abha_url,
                data=json.dumps({"healthId": health_id, "yearOfBirth": year_of_birth}),
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            available_status = resp.get("status")
            logging.info(f"{available_status=}")
            if resp_code <= 250:
                return resp
                # if resp.get("status") == True:
                #     return {"available": False}
                # return {"available": True}
            else:
                raise resp
        except Exception as error:
            logging.error(f"Error in HIDController.abha_verification function: {error}")
            raise error

    def abha_address_update(self, patient_id: str, abha_address: str):
        try:
            logging.info("executing  abha_address_update function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            patient_obj = self.CRUDPatientDetails.read_by_patientId(
                patient_id=patient_id
            )
            existing_abha_address = patient_obj.get("primary_abha_address")
            linking_token = patient_obj.get("linking_token").get("value")
            refresh_token = patient_obj.get("refresh_token").get("value")
            refresh_token_url = f"{self.abha_url}/v1/auth/generate/access-token"
            logging.info("Getting linking token")
            resp, resp_code = APIInterface().post(
                route=refresh_token_url,
                data=json.dumps({"refreshToken": refresh_token}),
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            linking_token = resp.get("accessToken", None)
            abha_update_url = f"{self.abha_url}/v2/account/phr-linked"
            logging.info("Updating abha_address on Gateway")
            resp, resp_code = APIInterface().post(
                route=abha_update_url,
                data=json.dumps({"phrAddress": abha_address, "preferred": True}),
                headers={
                    "Authorization": f"Bearer {gateway_access_token}",
                    "X-Token": f"Bearer {linking_token}",
                },
            )
            update_status = resp.get("status")
            logging.info(f"{update_status=}")
            logging.info(f"{resp_code=}")
            if resp_code <= 250:
                logging.info("Updating abha_address on database")
                self.CRUDPatientDetails.update(
                    **{
                        "id": patient_id,
                        "linking_token": {"value": linking_token},
                        "primary_abha_address": abha_address,
                    }
                )
                return {
                    "old_abha_address": existing_abha_address,
                    "new_abha_address": abha_address,
                    "update_status": update_status,
                }
            else:
                raise resp
        except Exception as error:
            logging.error(f"Error in HIDController.abha_verification function: {error}")
            raise error

    def abha_address_update_v1(self, patient_id: str, abha_address: str):
        try:
            logging.info("executing  abha_address_update function")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            patient_obj = self.CRUDPatientDetails.read_by_patientId(
                patient_id=patient_id
            )
            existing_abha_address = patient_obj.get("primary_abha_address")
            # linking_token = patient_obj.get("access_token").get("value")
            linking_token = patient_obj.get("linking_token").get("value")
            refresh_token = patient_obj.get("refresh_token").get("value")
            refresh_token_url = f"{self.abha_url}/v1/auth/generate/access-token"
            logging.info("Getting linking token")
            resp, resp_code = APIInterface().post(
                route=refresh_token_url,
                data=json.dumps({"refreshToken": refresh_token}),
                headers={"Authorization": f"Bearer {gateway_access_token}"},
            )
            linking_token = resp.get("accessToken", None)
            # abha_update_url = f"{self.abha_url}/v2/account/phr-linked"
            abha_update_url = f"{self.abha_url}/v1/account/profile"
            logging.info("Updating abha_address on Gateway")
            # resp, resp_code = APIInterface().post(
            #     route=abha_update_url,
            #     data=json.dumps({"phrAddress": abha_address, "preferred": True},
            #     headers={
            #         "Authorization": f"Bearer {gateway_access_token}",
            #         "X-Token": f"Bearer {linking_token}",
            #     },
            # )
            resp, resp_code = APIInterface().post(
                route=abha_update_url,
                data=json.dumps({"healthId": abha_address}),
                headers={
                    "Authorization": f"Bearer {gateway_access_token}",
                    "X-Token": f"Bearer {linking_token}",
                },
            )
            # update_status = resp.get("status")
            # logging.info(f"{update_status=}")
            logging.info(f"{resp_code=}")
            if resp_code <= 250:
                logging.info("Updating abha_address on database")
                self.CRUDPatientDetails.update(
                    **{
                        "id": patient_id,
                        "linking_token": {"value": linking_token},
                        "abha_address": abha_address,
                    }
                )
                # return {
                #     "old_abha_address": existing_abha_address,
                #     "new_abha_address": abha_address,
                #     "update_status": update_status,
                # }
                return resp
            else:
                raise resp
        except Exception as error:
            logging.error(f"Error in HIDController.abha_verification function: {error}")
            raise error

    def fetch_auth_modes(self, request):
        """[Controller to fetch patient auth modes]

        Args:
            request ([dict]): [fetch auth modes request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing  fetch_auth_modes function")
            request_dict = request.dict()
            logging.info("Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            fetch_modes_url = f"{self.gateway_url}/v0.5/users/auth/fetch-modes"
            request_id = str(uuid.uuid1())
            time_now = datetime.now(timezone.utc)
            time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
            fetch_mode_request = {
                "requestId": request_id,
                "timestamp": time_now,
                "query": {
                    "id": request_dict.get("abha_number"),
                    "purpose": request_dict.get("purpose"),
                    "requester": {"type": "HIP", "id": request_dict["hip_id"]},
                },
            }
            _, resp_code = APIInterface().post(
                route=fetch_modes_url,
                data=json.dumps(fetch_mode_request),
                headers={
                    "X-CM-ID": os.environ["X-CM-ID"],
                    "Authorization": f"Bearer {gateway_access_token}",
                    "Content-Type": "application/json",
                },
            )
            logging.debug(f"{resp_code=}")
            gateway_request = {
                "request_id": request_id,
                "request_type": "FETCH_AUTH_MODE",
            }
            if resp_code <= 250:
                gateway_request.update({"request_status": "PROCESSING"})
            else:
                gateway_request.update({"request_status": "FAILED"})
            self.CRUDGatewayInteraction.create(**gateway_request)
            gateway_request.update({"txn_id": request_id})
            return gateway_request
        except Exception as error:
            logging.error(
                f"Error in PatientController.fetch_auth_modes function: {error}"
            )
            raise error

    def auth_init(self, request):
        try:
            logging.info("executing  auth_init function")
            request_dict = request.dict()
            logging.info("Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            fetch_modes_url = f"{self.gateway_url}/v0.5/users/auth/init"
            request_id = str(uuid.uuid1())
            time_now = datetime.now(timezone.utc)
            time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
            _, resp_code = APIInterface().post(
                route=fetch_modes_url,
                data=json.dumps(
                    {
                        "requestId": request_id,
                        "timestamp": time_now,
                        "query": {
                            "id": request_dict.get("abha_number"),
                            "purpose": request_dict.get("purpose"),
                            "authMode": request_dict.get("auth_mode"),
                            "requester": {"type": "HIP", "id": request_dict["hip_id"]},
                        },
                    }
                ),
                headers={
                    "X-CM-ID": os.environ["X-CM-ID"],
                    "Authorization": f"Bearer {gateway_access_token}",
                    "Content-Type": "application/json",
                },
            )
            logging.debug(f"{resp_code=}")
            gateway_request = {
                "request_id": request_id,
                "request_type": "AUTH_INIT",
            }
            if resp_code <= 250:
                gateway_request.update({"request_status": "PROCESSING"})
            else:
                gateway_request.update({"request_status": "FAILED"})
            self.CRUDGatewayInteraction.create(**gateway_request)
            gateway_request.update({"txn_id": request_id})
            return gateway_request
        except Exception as error:
            logging.error(f"Error in PatientController.auth_init function: {error}")
            raise error

    def verify_otp(self, request):
        try:
            logging.info("executing  verify_otp function")
            request_dict = request.dict()
            logging.info("Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            auth_confirm_url = f"{self.gateway_url}/v0.5/users/auth/confirm"
            gateway_obj = self.CRUDGatewayInteraction.read(
                request_id=request_dict.get("txnId")
            )
            request_id = str(uuid.uuid1())
            time_now = datetime.now(timezone.utc)
            time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
            resp, resp_code = APIInterface().post(
                route=auth_confirm_url,
                data=json.dumps(
                    {
                        "requestId": request_id,
                        "timestamp": time_now,
                        "transactionId": gateway_obj.get("transaction_id"),
                        "credential": {"authCode": request_dict.get("otp")},
                    }
                ),
                headers={
                    "X-CM-ID": os.environ["X-CM-ID"],
                    "Authorization": f"Bearer {gateway_access_token}",
                    "Content-Type": "application/json",
                },
            )
            logging.debug(f"{resp_code=}")
            gateway_request = {
                "request_id": request_id,
                "request_type": "VERIFY_OTP",
            }
            if resp_code <= 250:
                gateway_request.update({"request_status": "PROCESSING"})
            else:
                gateway_request.update({"request_status": "FAILED"})
            self.CRUDGatewayInteraction.create(**gateway_request)
            return gateway_request
        except Exception as error:
            logging.error(f"Error in PatientController.verify_otp function: {error}")
            raise error

    def verify_demographic(self, request):
        try:
            logging.info("executing  verify_demographic function")
            request_dict = request.dict()
            logging.info(f"{request_dict=}")
            logging.info("Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            auth_confirm_url = f"{self.gateway_url}/v0.5/users/auth/confirm"
            logging.info(f"{request_dict.get('txnId')=}")
            gateway_obj = self.CRUDGatewayInteraction.read(
                request_id=request_dict.get("txnId")
            )
            logging.debug(f"{gateway_obj=}")
            request_id = str(uuid.uuid1())
            time_now = datetime.now(timezone.utc)
            time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
            resp, resp_code = APIInterface().post(
                route=auth_confirm_url,
                data=json.dumps(
                    {
                        "requestId": request_id,
                        "timestamp": time_now,
                        "transactionId": gateway_obj.get("transaction_id"),
                        "credential": {
                            "authCode": "",
                            "demographic": {
                                "name": request_dict.get("name"),
                                "gender": request_dict.get("gender"),
                                "dateOfBirth": request_dict.get("dateOfBirth"),
                                "identifier": {
                                    "type": "MOBILE",
                                    "value": request_dict.get("mobileNumber"),
                                },
                            },
                        },
                    }
                ),
                headers={
                    "X-CM-ID": os.environ["X-CM-ID"],
                    "Authorization": f"Bearer {gateway_access_token}",
                },
            )
            logging.debug(f"{resp_code=}")
            gateway_request = {
                "request_id": request_id,
                "request_type": "VERIFY_DEMOGRAPHIC",
            }
            if resp_code <= 250:
                gateway_request.update({"request_status": "PROCESSING"})
            else:
                gateway_request.update({"request_status": "FAILED"})
            self.CRUDGatewayInteraction.create(**gateway_request)
            return gateway_request
        except Exception as error:
            logging.error(
                f"Error in PatientController.verify_demographic function: {error}"
            )
            raise error

    def patient_share(self, request, hip_id):
        try:
            logging.info("executing  patient_share function")
            logging.info("Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            patient_data = request.get("profile").get("patient")
            logging.info("Getting identifiers")
            for idf in patient_data.get("identifiers"):
                if idf["type"] == "MOBILE":
                    mobile_number = idf["value"]
                if idf["type"] == "EMAIL":
                    email_id = idf["value"]
            dob_str = f"{patient_data['yearOfBirth']}-{patient_data['monthOfBirth']}-{patient_data['dayOfBirth']}"
            patient_obj = FuzzyMatch().find_duplicate_record(
                mobile_number=mobile_number,
                name=patient_data.get("name"),
                dob=dob_str,
                gender=patient_data.get("gender"),
                hip_id=hip_id,
            )
            abha_number = patient_data.get("healthIdNumber")
            patient_request = {
                "abha_number": abha_number,
                "abha_address": patient_data["healthId"],
                "mobile_number": mobile_number,
                "name": patient_data["name"],
                "gender": patient_data["gender"],
                "DOB": dob_str,
                "year_of_birth": patient_data["yearOfBirth"],
                "email": email_id,
                "address": patient_data["address"]["line"],
                "district": patient_data["address"]["district"],
                "pincode": patient_data["address"]["pincode"],
                "state_name": patient_data["address"]["state"],
                "auth_methods": {"authMethods": ["AADHAAR_OTP", "MOBILE_OTP"]},
                "hip_id": hip_id,
                "abha_status": "ACTIVE",
                "is_verified": False,
            }
            if patient_obj is None:
                patient_id = f"C360-PID-{str(uuid.uuid1().int)[:18]}"
                patient_request.update({"id": patient_id})
                self.CRUDPatientDetails.create(**patient_request)
            else:
                patient_request.update({"id": patient_obj["id"]})
                self.CRUDPatientDetails.update(**patient_request)
            akw_url = f"{self.gateway_url}/v1.0/patients/profile/on-share"
            request_id = str(uuid.uuid1())
            time_now = datetime.now(timezone.utc)
            time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
            resp, resp_code = APIInterface().post(
                route=akw_url,
                data=json.dumps(
                    {
                        "requestId": request_id,
                        "timestamp": time_now,
                        "acknowledgement": {
                            "status": "SUCCESS",
                            "healthId": patient_data.get("healthId"),
                            "tokenNumber": "122",
                        },
                        "error": None,
                        "resp": {"requestId": request.get("requestId")},
                    }
                ),
                headers={
                    "X-CM-ID": os.environ["X-CM-ID"],
                    "Authorization": f"Bearer {gateway_access_token}",
                },
            )
            logging.debug(f"{resp_code=}")
            logging.debug(f"{resp=}")
            return {"status": resp_code, "statusText": resp, "data": resp}
        except Exception as error:
            logging.error(f"Error in PatientController.patient_share function: {error}")
            raise error

    def verify_patient(self, request):
        try:
            logging.info("executing  verify_patient function")
            self.CRUDPatientDetails.update(
                **{"id": request.patient_id, "is_verified": True}
            )
            return {"patient_id": request.patient_id, "is_verified": True}
        except Exception as error:
            logging.error(
                f"Error in PatientController.verify_patient function: {error}"
            )
            raise error

    def discover_patient(self, request, hip_id):
        try:
            care_context = []
            logging.info("executing  discover_patient function")
            logging.info("creating gateway record")
            txn_id = request.get("transactionId")
            req_id = request.get("requestId")
            self.CRUDGatewayInteraction.create(
                **{
                    "request_id": req_id,
                    "request_type": "PATIENT_DISCOVER",
                    "request_status": "PROCESSING",
                    "transaction_id": txn_id,
                }
            )
            logging.info("Starting Fuzzy matching")
            hip_obj = self.CRUDHIP.read(hip_ip=hip_id)
            if hip_obj:
                logging.info("Getting session access Token")
                gateway_access_token = get_session_token(
                    session_parameter="gateway_token"
                ).get("accessToken")
                on_discover_url = f"{self.gateway_url}/v0.5/care-contexts/on-discover"
                matching_results = FuzzyMatch().find_record(
                    request=request, hip_id=hip_id
                )
                logging.info(f"{matching_results=}")
                logging.info(f"{len(matching_results)=}")
                if len(matching_results) > 1:
                    logging.info("more than one definitive match for the given request")
                    resp, resp_code = APIInterface().post(
                        route=on_discover_url,
                        data=json.dumps(
                            {
                                "requestId": str(uuid.uuid1()),
                                "timestamp": datetime.now(timezone.utc).strftime(
                                    "%Y-%m-%dT%H:%M:%S.%f"
                                ),
                                "transactionId": txn_id,
                                "patient": None,
                                "error": {
                                    "code": 1000,
                                    "message": "more than one definitive match for the given request",
                                },
                                "resp": {"requestId": req_id},
                            }
                        ),
                        headers={
                            "X-CM-ID": os.environ["X-CM-ID"],
                            "Authorization": f"Bearer {gateway_access_token}",
                        },
                    )
                    self.CRUDGatewayInteraction.update(
                        **{
                            "request_id": req_id,
                            "request_status": "FAILED",
                            "error_code": "1000",
                            "error_message": "more than one definitive match for the given request",
                        }
                    )
                elif len(matching_results) == 0:
                    logging.info("no verified identifer was specified")
                    resp, resp_code = APIInterface().post(
                        route=on_discover_url,
                        data=json.dumps(
                            {
                                "requestId": str(uuid.uuid1()),
                                "timestamp": datetime.now(timezone.utc).strftime(
                                    "%Y-%m-%dT%H:%M:%S.%f"
                                ),
                                "transactionId": txn_id,
                                "patient": None,
                                "error": {
                                    "code": 1000,
                                    "message": "no verified identifer was specified",
                                },
                                "resp": {"requestId": req_id},
                            }
                        ),
                        headers={
                            "X-CM-ID": os.environ["X-CM-ID"],
                            "Authorization": f"Bearer {gateway_access_token}",
                        },
                    )
                    self.CRUDGatewayInteraction.update(
                        **{
                            "request_id": req_id,
                            "request_status": "FAILED",
                            "error_code": "1000",
                            "error_message": "no verified identifer was specified",
                        }
                    )
                else:
                    logging.info("Exactly 1 record found")
                    logging.info("Getting Patient Id")
                    patient_id = list(matching_results.keys())[0]
                    logging.info(f"{patient_id=}")
                    logging.info("Getting PMR records for patient")
                    pmr_record = self.CRUDPatientMedicalRecord.read_by_patientId(
                        patient_id=patient_id
                    )
                    logging.info(f"{pmr_record=}")
                    for pmr in pmr_record:
                        care_context.append(
                            {
                                "referenceNumber": f"{hip_obj['hip_uid']}-{pmr['id']}",
                                "display": f"Consultation Record for {pmr['date_of_consultation']}",
                            }
                        )
                    resp, resp_code = APIInterface().post(
                        route=on_discover_url,
                        data=json.dumps(
                            {
                                "requestId": str(uuid.uuid1()),
                                "timestamp": datetime.now(timezone.utc).strftime(
                                    "%Y-%m-%dT%H:%M:%S.%f"
                                ),
                                "transactionId": txn_id,
                                "patient": {
                                    "referenceNumber": patient_id,
                                    "display": matching_results[patient_id]["name"],
                                    "careContexts": care_context,
                                    "matchedBy": [
                                        matching_results[patient_id]["matched_by"]
                                    ],
                                },
                                "error": None,
                                "resp": {"requestId": req_id},
                            }
                        ),
                        headers={
                            "X-CM-ID": os.environ["X-CM-ID"],
                            "Authorization": f"Bearer {gateway_access_token}",
                            "Content-Type": "application/json",
                        },
                    )
                    logging.debug(f"{resp_code=}")
                    logging.debug(f"{resp=}")
                    gateway_request = {"request_id": req_id}
                    if resp_code <= 250:
                        gateway_request.update({"request_status": "PROCESSING"})
                    else:
                        gateway_request.update({"request_status": "FAILED"})
                    self.CRUDGatewayInteraction.update(**gateway_request)
                    return gateway_request
        except Exception as error:
            logging.error(
                f"Error in PatientController.discover_patient function: {error}"
            )
            raise error

    def link_patient(self, request, hip_id):
        try:
            logging.info("executing  link_patient function")
            logging.info("Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            logging.info("Getting transactionId")
            txn_id = request.get("transactionId")
            patient_obj = request.get("patient")
            patient_id = patient_obj.get("referenceNumber")
            patient_details = self.CRUDPatientDetails.read_by_patientId(
                patient_id=patient_id
            )
            patient_mobile_number = patient_details.get("mobile_number")
            pmr_list = []
            for pmr in patient_obj.get("careContexts"):
                pmr_id = pmr.get("referenceNumber")
                pmr_list.append(pmr_id)
            logging.info("Generating on-init request")
            otp_ref_num = str(uuid.uuid1())
            otp = str(uuid.uuid1().int)[-6:]
            time_change = timedelta(minutes=15)
            expiry_time = datetime.now(pytz_timezone("Asia/Kolkata")) + time_change
            otp_expiry_time = expiry_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
            payload = {
                "requestId": str(uuid.uuid1()),
                "timestamp": datetime.now(timezone.utc).strftime(
                    "%Y-%m-%dT%H:%M:%S.%f"
                ),
                "transactionId": txn_id,
                "link": {
                    "referenceNumber": otp_ref_num,
                    "authenticationType": "DIRECT",
                    "meta": {
                        "communicationMedium": "MOBILE",
                        "communicationHint": "string",
                        "communicationExpiry": otp_expiry_time,
                    },
                },
                "error": None,
                "resp": {"requestId": request.get("requestId")},
            }
            otp_response = otpHelper().send_otp(
                mobile_number=patient_mobile_number,
                otp=otp,
                template_id=self.msg91_template_id,
            )
            linking_on_init_url = f"{self.gateway_url}/v0.5/links/link/on-init"
            resp, resp_code = APIInterface().post(
                route=linking_on_init_url,
                data=json.dumps(payload),
                headers={
                    "X-CM-ID": os.environ["X-CM-ID"],
                    "Authorization": f"Bearer {gateway_access_token}",
                },
            )
            logging.debug(f"{resp_code=}")
            logging.debug(f"{resp=}")
            self.CRUDGatewayInteraction.create(
                **{
                    "request_id": otp_ref_num,
                    "request_type": "LINK_OTP_VERIFICATION",
                    "request_status": "PROCESSING",
                    "transaction_id": txn_id,
                    "gateway_metadata": {
                        "patient_mobile_number": patient_mobile_number,
                        "otp": otp,
                        "otp_expiry": otp_expiry_time,
                        "pmr_list": pmr_list,
                        "patient_id": patient_id,
                    },
                }
            )
        except Exception as error:
            logging.error(f"Error in PatientController.link_patient function: {error}")
            raise error

    def link_confirm(self, request, hip_id):
        try:
            logging.info("executing  link_confirm function")
            logging.info("Getting session access Token")
            gateway_access_token = get_session_token(
                session_parameter="gateway_token"
            ).get("accessToken")
            logging.info("Getting confirmation details")
            link_ref_num = request.get("confirmation").get("linkRefNumber")
            otp = request.get("confirmation").get("token")
            gateway_obj = self.CRUDGatewayInteraction.read(request_id=link_ref_num)
            logging.info(f"{gateway_obj=}")
            gateway_meta = gateway_obj.get("gateway_metadata")
            patient_mobile_number = gateway_meta.get("patient_mobile_number")
            otp_verification_response = otpHelper().verify_otp(
                mobile_number=patient_mobile_number, otp=otp
            )
            if otp_verification_response.get("type") == "success":
                # if otp == gateway_meta.get("otp"):
                logging.info("OTP verified")
                logging.info("Getting Patient Record")
                patient_obj = self.CRUDPatientDetails.read_by_patientId(
                    patient_id=gateway_meta.get("patient_id")
                )
                logging.info("Getting PMR Id")
                careContext = []
                logging.info(f"{hip_id=}")
                for pmr_id in gateway_meta.get("pmr_list"):
                    pmr_id = pmr_id.split("-", 1)[1]
                    logging.info(f"{pmr_id=}")
                    pmr_obj = self.CRUDPatientMedicalRecord.read(pmr_id=pmr_id)
                    logging.info(f"{pmr_obj=}")
                    careContext.append(
                        {
                            "referenceNumber": pmr_id,
                            "display": f"Consultation Record for {pmr_obj['date_of_consultation']}",
                        }
                    )
                payload = {
                    "requestId": str(uuid.uuid1()),
                    "timestamp": datetime.now(timezone.utc).strftime(
                        "%Y-%m-%dT%H:%M:%S.%f"
                    ),
                    "patient": {
                        "referenceNumber": patient_obj["id"],
                        "display": patient_obj["name"],
                        "careContexts": careContext,
                    },
                    "error": None,
                    "resp": {"requestId": request.get("requestId")},
                }
                self.CRUDGatewayInteraction.update(
                    **{"request_id": link_ref_num, "request_status": "SUCCESS"}
                )
                linking_on_init_url = f"{self.gateway_url}/v0.5/links/link/on-confirm"
                resp, resp_code = APIInterface().post(
                    route=linking_on_init_url,
                    data=json.dumps(payload),
                    headers={
                        "X-CM-ID": os.environ["X-CM-ID"],
                        "Authorization": f"Bearer {gateway_access_token}",
                    },
                )
                logging.debug(f"{resp_code=}")
                logging.debug(f"{resp=}")
                if resp_code < 300:
                    for pmr_id in gateway_meta.get("pmr_list"):
                        self.CRUDPatientMedicalRecord.update(
                            **{"id": pmr_id, "abdm_linked": True}
                        )
            else:
                logging.info("Invalid OTP")
                payload = {
                    "requestId": str(uuid.uuid1()),
                    "timestamp": datetime.now(timezone.utc).strftime(
                        "%Y-%m-%dT%H:%M:%S.%f"
                    ),
                    "patient": None,
                    "error": {"code": 403, "message": "Invalid OTP"},
                    "resp": {"requestId": request.get("requestId")},
                }
                self.CRUDGatewayInteraction.update(
                    **{
                        "request_id": link_ref_num,
                        "request_status": "FAILED",
                        "error_message": "Invalid OTP",
                        "error_code": "403",
                    }
                )
                linking_on_init_url = f"{self.gateway_url}/v0.5/links/link/on-confirm"
                resp, resp_code = APIInterface().post(
                    route=linking_on_init_url,
                    data=json.dumps(payload),
                    headers={
                        "X-CM-ID": os.environ["X-CM-ID"],
                        "Authorization": f"Bearer {gateway_access_token}",
                    },
                )
                logging.debug(f"{resp_code=}")
                logging.debug(f"{resp=}")
        except Exception as error:
            logging.error(f"Error in PatientController.link_confirm function: {error}")
            raise error

    def register_patient_controller(self, request):
        """[Controller to register new user]

        Args:
            request ([dict]): [create new user request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing register new patient function")
            request_json = request.dict()
            dob_str = request_json.get("DOB")
            # dob_obj = datetime.strptime(dob_str, "%Y-%m-%d")
            # dob_str = dob_obj.strftime("%d/%m/%Y")
            patient_obj = FuzzyMatch().find_duplicate_record(
                mobile_number=request_json["mobile_number"],
                name=request_json["name"],
                dob=dob_str,
                gender=request_json["gender"],
                hip_id=request_json["hip_id"],
            )
            if patient_obj:
                patient_obj.update({"status": "Patient already exist"})
                request_json.update({"id": patient_obj["id"], "is_verified": True})
                self.CRUDPatientDetails.update(**request_json)
                return patient_obj
            else:
                patient_id = f"C360-PID-{str(uuid.uuid1().int)[:18]}"
                request_json.update({"id": patient_id, "is_verified": True})
                self.CRUDPatientDetails.create(**request_json)
                request_json.update({"status": "New Patient created successfully"})
                return request_json
        except Exception as error:
            logging.error(f"Error in register_patient_controller function: {error}")
            raise error

    def register_patient_v3_controller(self, request):
        """[Controller to register new user]

        Args:
            request ([dict]): [create new user request]

        Raises:
            error: [Error raised from controller layer]

        Returns:
            [dict]: [authorization details]
        """
        try:
            logging.info("executing register new patient v3 function")
            request_json = request.dict()
            request_json.update(
                {"auth_methods": {"authMethods": ["AADHAAR_OTP", "MOBILE_OTP"]}}
            )
            dob_str = request_json.get("DOB")
            age_str = request_json.get("age")
            if dob_str:
                yob_str = dob_str.split("-")[-1]
                dob_obj = datetime.strptime(dob_str, "%d-%m-%Y")
                dob_str = dob_obj.strftime("%Y-%m-%d")
            elif age_str:
                today = datetime.today()
                yob_str = today.year - int(age_str)
            patient_obj = FuzzyMatch().find_duplicate_record(
                mobile_number=request_json.get("mobile_number"),
                name=request_json.get("name"),
                yob=yob_str,
                gender=request_json.get("gender"),
                hip_id=request_json.get("hip_id"),
            )
            request_json.update({"DOB": dob_str, "year_of_birth": yob_str})
            if patient_obj:
                request_json.update({"id": patient_obj["id"], "is_verified": True})
                self.CRUDPatientDetails.update(**request_json)
                request_json.update(
                    {"status": "Patient already exist, Updated database"}
                )
                return request_json
            else:
                patient_id = f"C360-PID-{str(uuid.uuid1().int)[:18]}"
                request_json.update({"id": patient_id, "is_verified": True})
                self.CRUDPatientDetails.create(**request_json)
                request_json.update({"status": "New Patient created successfully"})
                return request_json
        except Exception as error:
            logging.error(f"Error in register_patient_controller function: {error}")
            raise error

    def update_patient(self, request):
        try:
            logging.info("Updating patient records")
            # for patient_obj in request.data:
            patient_obj_dict = request.dict()
            patient_obj_dict.pop("pid")
            self.CRUDPatientDetails.update(**patient_obj_dict, id=request.pid)
            return {"patient_id": request.pid}
        except Exception as error:
            logging.error(
                f"Error in PatientController.update_patient function: {error}"
            )
            raise error

    def delete_patient(self, patient_id):
        try:
            logging.info("Deleting patient records")
            # for patient_obj in request.data:
            deleted_patient = self.CRUDPatientDetails.delete(patient_id=patient_id)
            return deleted_patient
        except Exception as error:
            logging.error(
                f"Error in PatientController.delete_patient function: {error}"
            )
            raise error

    def get_patient_details(self, patient_id: str):
        try:
            logging.info("executing get_patient_details function")
            patient_obj = self.CRUDPatientDetails.read_by_patientId(
                patient_id=patient_id
            )
            if patient_obj.get("DOB", None):
                dob_obj = datetime.strptime(patient_obj["DOB"], "%Y-%m-%d")
                age_in_years, age_in_months = calculate_age(dob=dob_obj)
                patient_obj["age_in_years"] = age_in_years
                patient_obj["age_in_months"] = age_in_months
            else:
                patient_obj["age_in_years"] = datetime.today().year - int(
                    patient_obj["year_of_birth"]
                )
            return patient_obj
        except Exception as error:
            logging.error(f"Error in get_patient_details function: {error}")
            raise error

    def list_all_patients(self, hip_id: str):
        try:
            logging.info("executing list_all_patients function")
            patient_obj = self.CRUDPatientDetails.read_all(hip_id=hip_id)
            return patient_obj
        except Exception as error:
            logging.error(f"Error in list_all_patients function: {error}")
            raise error

    def get_vital(self, patient_id, vital_type):
        try:
            logging.info("Get vital records")
            responses = self.CRUDVital.read_by_patientId(patient_id)
            values = []
            for response in responses:
                vital_obj = {}
                vital_obj["value"] = response[vital_type]
                vital_obj["pmr_id"] = response["pmr_id"]
                date = response["created_at"].strftime("%Y-%m-%d %H:%M")
                vital_obj["created_date"] = date

                values.append(vital_obj)
                # logging.info(f"{vital_obj=}")
                # logging.info(f"{values=}")
            return values
        except Exception as error:
            logging.error(f"Error in PatientController.get_vital function: {error}")
            raise error
