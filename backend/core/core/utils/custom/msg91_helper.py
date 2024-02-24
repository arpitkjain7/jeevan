from core.utils.custom.external_call import APIInterface
from core import logger
import os

logging = logger(__name__)


class otpHelper:
    def __init__(self):
        self.msg91_base_url = os.environ["msg91_base_url"]
        self.msg91_auth_key = os.environ["msg91_auth_key"]

    def send_otp(self, mobile_number: str, otp: str, template_id: str):
        try:
            if len(mobile_number) == 10:
                mobile_number = f"91{mobile_number}"
            send_otp_params = {
                "template_id": template_id,
                "mobile": int(mobile_number),
                "otp": str(otp),
            }
            auth_header = {"authkey": self.msg91_auth_key}
            send_otp_url = f"{self.msg91_base_url}/v5/otp"
            response, status_code = APIInterface().post_with_params(
                route=send_otp_url, params=send_otp_params, headers=auth_header
            )
            return response
        except Exception as error:
            logging.error(f"Error in send_otp function: {error}")
            raise error

    def verify_otp(self, mobile_number: str, otp: int):
        try:
            if len(mobile_number) == 10:
                mobile_number = f"91{mobile_number}"
            verify_otp_params = {
                "mobile": int(mobile_number),
                "otp": otp,
            }
            auth_header = {"authkey": self.msg91_auth_key}
            verify_otp_url = f"{self.msg91_base_url}/v5/otp/verify"
            response, status_code = APIInterface().get(
                route=verify_otp_url,
                params=verify_otp_params,
                headers=auth_header,
            )
            return response
        except Exception as error:
            logging.error(f"Error in verify_otp function: {error}")
            raise error

    def resend_otp(self, mobile_number: str, otp: int):
        try:
            if len(mobile_number) == 10:
                mobile_number = f"91{mobile_number}"
            verify_otp_params = {"mobile": int(mobile_number)}
            auth_header = {"authkey": self.msg91_auth_key}
            resend_otp_url = f"{self.msg91_base_url}/v5/otp/retry"
            response, status_code = APIInterface().get(
                route=resend_otp_url,
                params=verify_otp_params,
                headers=auth_header,
            )
            return response
        except Exception as error:
            logging.error(f"Error in send_otp function: {error}")
            raise error


class smsHelper:
    def __init__(self):
        self.msg91_base_url = os.environ["msg91_base_url"]
        self.msg91_auth_key = os.environ["msg91_auth_key"]
        self.msg91_send_health_record_template_id = os.environ[
            "msg91_send_health_record_template_id"
        ]

    def send_prescription(
        self, mobile_number: str, hospital_name: str, document_url: str
    ):
        try:
            if len(mobile_number) == 10:
                mobile_number = f"91{mobile_number}"
            payload = {"mobile": int(mobile_number)}
            payload = {
                "template_id": self.msg91_send_health_record_template_id,
                "short_url": "1",
                "recipients": [
                    {
                        "mobiles": int(mobile_number),
                        "hospital_name": hospital_name,
                        "document_url": document_url,
                    }
                ],
            }
            auth_header = {
                "accept": "application/json",
                "content-type": "application/json",
                "authkey": self.msg91_auth_key,
            }
            send_sms_url = f"{self.msg91_base_url}/v5/flow"
            response, status_code = APIInterface().post_v1(
                route=send_sms_url,
                json=payload,
                headers=auth_header,
            )
            return response, status_code
        except Exception as error:
            logging.error(f"Error in send_health_record function: {error}")
            raise error
