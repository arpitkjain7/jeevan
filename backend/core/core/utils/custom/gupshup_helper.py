from core.utils.custom.external_call import APIInterface
from core import logger
from urllib.parse import urlencode
import os
import json

logging = logger(__name__)


class whatsappHelper:
    def __init__(self):
        self.gupshup_base_url = os.environ["gupshup_base_url"]
        self.gupshup_api_key = os.environ["gupshup_api_key"]
        self.gupshup_notification_template = os.environ["gupshup_notification_template"]
        self.gupshup_appointment_notification_template = os.environ["gupshup_appointment_notification_template"]
        self.gupshup_google_review_template = os.environ[
            "gupshup_google_review_template"
        ]

    def optin_user(self, mobile_number: str):
        try:
            if len(mobile_number) == 10:
                mobile_number = f"91{mobile_number}"
            optin_payload = {"user": int(mobile_number)}
            optin_router = f"{self.gupshup_base_url}/sm/api/v1/app/opt/in/CliniQ360"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "apikey": self.gupshup_api_key,
            }
            response, status_code = APIInterface().post(
                route=optin_router, data=optin_payload, headers=headers
            )
            return response, status_code
        except Exception as error:
            logging.error(f"Error in optin_user function: {error}")
            raise error

    def send_prescription(
        self,
        mobile_number: str,
        document_url: str,
        patient_name: str,
        hospital_name: str,
        date_of_consultation: str,
    ):
        try:
            if len(mobile_number) == 10:
                mobile_number = f"91{mobile_number}"
            payload = {
                "channel": "whatsapp",
                "source": 918329655340,
                "destination": int(mobile_number),
                "src.name": "CliniQ360",
            }
            payload["template"] = json.dumps(
                {
                    "id": self.gupshup_notification_template,
                    "params": [patient_name, hospital_name],
                }
            )
            payload["message"] = json.dumps(
                {
                    "type": "document",
                    "document": {
                        "link": document_url,
                        "filename": f"Prescription {date_of_consultation.date()}",
                    },
                },
            )
            flat_payload = {
                key: val if not isinstance(val, dict) else json.dumps(val)
                for key, val in payload.items()
            }
            # Convert the Python dictionary to a URL-encoded string
            payload_encoded = urlencode(flat_payload)
            headers = {
                "Cache-Control": "no-cache",
                "Content-Type": "application/x-www-form-urlencoded",
                "apikey": self.gupshup_api_key,
                "cache-control": "no-cache",
            }
            send_document_router = f"{self.gupshup_base_url}/wa/api/v1/template/msg"
            response, status_code = APIInterface().post_v1(
                route=send_document_router,
                data=payload_encoded,
                headers=headers,
            )
            return response, status_code
        except Exception as error:
            logging.error(f"Error in send_prescription function: {error}")
            raise error

    def send_google_review_link(
        self,
        mobile_number: str,
    ):
        try:
            if len(mobile_number) == 10:
                mobile_number = f"91{mobile_number}"
            payload = {
                "channel": "whatsapp",
                "source": 918329655340,
                "destination": int(mobile_number),
                "src.name": "CliniQ360",
            }
            payload["template"] = json.dumps(
                {"id": self.gupshup_google_review_template, "params": []}
            )
            flat_payload = {
                key: val if not isinstance(val, dict) else json.dumps(val)
                for key, val in payload.items()
            }
            # Convert the Python dictionary to a URL-encoded string
            payload_encoded = urlencode(flat_payload)
            headers = {
                "Cache-Control": "no-cache",
                "Content-Type": "application/x-www-form-urlencoded",
                "apikey": self.gupshup_api_key,
                "cache-control": "no-cache",
            }
            send_google_review_link = f"{self.gupshup_base_url}/wa/api/v1/template/msg"
            response, status_code = APIInterface().post_v1(
                route=send_google_review_link,
                data=payload_encoded,
                headers=headers,
            )
            return response, status_code
        except Exception as error:
            logging.error(f"Error in send_google_review_link function: {error}")
            raise error


    def send_appointment_list(
        self,
        mobile_number: str, 
        destination_mobile_number: str,
        patient_name: str,
        app_date: str,
        doc_name: str,
    ):
        try:
            if len(destination_mobile_number) == 10:
               destination_mobile_number = f"91{destination_mobile_number}"
            payload = {
                "channel": "whatsapp",
                "source": 918329655340,
                "destination": int(destination_mobile_number),
                "src.name": "CliniQ360",
            }
            payload["template"] = json.dumps(
                {"id": self.gupshup_appointment_notification_template , "params": [doc_name,app_date,patient_name, mobile_number ]}
            )
            flat_payload = {
                key: val if not isinstance(val, dict) else json.dumps(val)
                for key, val in payload.items()
            }
            # Convert the Python dictionary to a URL-encoded string
            payload_encoded = urlencode(flat_payload)
            headers = {
                "Cache-Control": "no-cache",
                "Content-Type": "application/x-www-form-urlencoded",
                "apikey": self.gupshup_api_key,
                "cache-control": "no-cache",
            }
            send_appointment_list_link = f"{self.gupshup_base_url}/wa/api/v1/template/msg"
            response, status_code = APIInterface().post_v1(
                route=send_appointment_list_link,
                data=payload_encoded,
                headers=headers,
            )
            return response, status_code
        except Exception as error:
            logging.error(f"Error in send_appointment_list function: {error}")
            raise error