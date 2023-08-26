from gateway.crud.hims_patientDetails_crud import CRUDPatientDetails
from gateway.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
from gateway.crud.hims_hip_crud import CRUDHIP
from gateway.crud.hims_patientMedicalRecord_crud import CRUDPatientMedicalRecord
from gateway.utils.custom.external_call import APIInterface
from gateway.utils.custom.msg91_helper import otpHelper
from gateway.utils.custom.session_helper import get_session_token
from gateway import logger
from gateway.utils.custom.fuzzy_match import FuzzyMatch
from datetime import datetime, timezone, timedelta
import os
import uuid
from pytz import timezone as pytz_timezone

logging = logger(__name__)


class PatientCallbackController:
    def __init__(self):
        self.CRUDPatientDetails = CRUDPatientDetails()
        self.CRUDGatewayInteraction = CRUDGatewayInteraction()
        self.CRUDHIP = CRUDHIP()
        self.CRUDPatientMedicalRecord = CRUDPatientMedicalRecord()
        self.gateway_url = os.environ["gateway_url"]

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
            patient_obj = self.CRUDPatientDetails.read_by_abhaAddress(
                abha_address=patient_data.get("healthId")
            )
            if patient_obj is None:
                abha_number = patient_data.get("healthIdNumber")
                if abha_number:
                    abha_number = abha_number.replace("-", "")
                patient_id = f"C360-PID-{str(uuid.uuid1().int)[:18]}"
                patient_request = {
                    "id": patient_id,
                    "abha_number": abha_number,
                    "abha_address": patient_data["healthId"],
                    "mobile_number": mobile_number,
                    "name": patient_data["name"],
                    "gender": patient_data["gender"],
                    "DOB": f"{patient_data['dayOfBirth']}/{patient_data['monthOfBirth']}/{patient_data['yearOfBirth']}",
                    "email": email_id,
                    "address": patient_data["address"]["line"],
                    "district": patient_data["address"]["district"],
                    "pincode": patient_data["address"]["pincode"],
                    "state_name": patient_data["address"]["state"],
                    "hip_id": hip_id,
                    "abha_status": "ACTIVE",
                }
                self.CRUDPatientDetails.create(**patient_request)
            akw_url = f"{self.gateway_url}/v1.0/patients/profile/on-share"
            request_id = str(uuid.uuid1())
            time_now = datetime.now(timezone.utc)
            time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
            resp, resp_code = APIInterface().post(
                route=akw_url,
                data={
                    "requestId": request_id,
                    "timestamp": time_now,
                    "acknowledgement": {
                        "status": "SUCCESS",
                        "healthId": patient_data.get("healthId"),
                        "tokenNumber": "122",
                    },
                    "error": None,
                    "resp": {"requestId": request.get("requestId")},
                },
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
                matching_results = FuzzyMatch().find_record(request)
                logging.info(f"{matching_results=}")
                logging.info(f"{len(matching_results)=}")
                if len(matching_results) > 1:
                    logging.info("more than one definitive match for the given request")
                    resp, resp_code = APIInterface().post(
                        route=on_discover_url,
                        data={
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
                        },
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
                        data={
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
                        },
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
                        data={
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
                        },
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
            patient_details = CRUDPatientDetails().read_by_patientId(
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
                mobile_number=patient_mobile_number, otp=otp
            )
            linking_on_init_url = f"{self.gateway_url}/v0.5/links/link/on-init"
            resp, resp_code = APIInterface().post(
                route=linking_on_init_url,
                data=payload,
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
                    data=payload,
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
                            pmr_id=pmr_id, **{"abdm_linked": True}
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
                    data=payload,
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

    def deep_link_ack(self, request: dict):
        try:
            logging.info("executing  deep_link_ack function")
            logging.info("Getting request id")
            request_id = request.get("resp").get("requestId")
            logging.info("Getting error message")
            error_message = request.get("error")
            logging.info(f"{error_message=}")
            if error_message:
                gateway_request = {
                    "request_id": request_id,
                    "callback_response": request,
                    "request_status": "FAILED",
                    "error_code": error_message.get("code", 000),
                    "error_message": error_message.get("message", None),
                }
            else:
                gateway_request = {
                    "request_id": request_id,
                    "callback_response": request,
                    "request_status": "SUCESS",
                }
            self.CRUDGatewayInteraction.update(**gateway_request)
            return {"status": "trigger success"}
        except Exception as error:
            logging.error(f"Error in PMRController.deep_link_ack function: {error}")
            raise error
