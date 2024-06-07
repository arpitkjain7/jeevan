import json
from external_call import APIInterface
import os
from datetime import datetime, timedelta
from gupshup_helper import whatsappHelper
from auth import decodePayload
import requests

base_url = os.environ["callback_base_url"]
service_user = os.environ["service_user"]
service_password = os.environ["service_password"]


def send_followup_notifications(event, context):
    today = datetime.now()
    next_day = today + timedelta(days=1)
    next_date = next_day.date()
    next_date_str = next_date.strftime("%Y-%m-%d")
    login_endpoint = f"{base_url}/v1/user/signIn"
    login_payload = {"username": service_user, "password": service_password}
    login_resp, status_code = APIInterface().post(
        route=login_endpoint,
        data=login_payload,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
    )
    access_token = login_resp.get("access_token")
    get_followup_endpoint = f"{base_url}/v1/appointment/listFollowUpByDate"
    follow_up_data, status_code = APIInterface().get(
        route=get_followup_endpoint,
        params={"appointment_date": next_date_str},
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    encrypted_data = follow_up_data.get("follow_up")
    decoded_payload = decodePayload(encrypted_payload=encrypted_data)
    msg_list = []
    print(f"{decoded_payload=}")
    follow_up_list = decoded_payload.get("data")
    for followup_obj in follow_up_list:
        print(f"{followup_obj=}")
        # if followup_obj.get("hip_id") == "123123":
        print(f"{followup_obj=}")
        opt_in_response, opt_in_status_code = whatsappHelper().optin_user(
            mobile_number=followup_obj.get("patient_contact_number")
        )
        print(f"{opt_in_response=} | {opt_in_status_code=}")
        msg_resp, resp_code = whatsappHelper().send_followup_notification(
            mobile_number=followup_obj.get("patient_contact_number"),
            patient_name=followup_obj.get("patient_name"),
            hospital_name=followup_obj.get("hip_name"),
            doctor_name=followup_obj.get("doctor_name"),
            hospital_contact_number=followup_obj.get("hip_contact_number"),
            followup_date=followup_obj.get("followup_date"),
        )
        msg_list.append(msg_resp)
    print(f"{msg_list=}")
    return {"statusCode": 200, "body": msg_list}
