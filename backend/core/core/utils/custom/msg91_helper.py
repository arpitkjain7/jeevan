from core.utils.custom.external_call import APIInterface
from core import logger
import os

logging = logger(__name__)


class otpHelper:
    def __init__(self):
        self.msg91_base_url = os.environ["msg91_base_url"]
        self.msg91_auth_key = os.environ["msg91_auth_key"]
        self.msg91_template_id = os.environ["msg91_template_id"]

    def send_otp(self, mobile_number: str, otp: int):
        try:
            if len(mobile_number) == 10:
                mobile_number = f"91{mobile_number}"
            send_otp_params = {
                "template_id": self.msg91_template_id,
                "mobile": int(mobile_number),
                "otp": int(otp),
            }
            auth_header = {"authkey": self.msg91_auth_key}
            response, status_code = APIInterface().post_with_params(
                route=self.msg91_base_url, params=send_otp_params, headers=auth_header
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
                "otp": int(otp),
            }
            auth_header = {"authkey": self.msg91_auth_key}
            response, status_code = APIInterface().get(
                route=f"{self.msg91_base_url}/verify",
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
            response, status_code = APIInterface().get(
                route=f"{self.msg91_base_url}/retry",
                params=verify_otp_params,
                headers=auth_header,
            )
            return response
        except Exception as error:
            logging.error(f"Error in send_otp function: {error}")
            raise error
