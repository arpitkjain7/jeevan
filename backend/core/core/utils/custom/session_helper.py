from core.utils.custom.external_call import APIInterface
from core.crud.hrp_session_crud import CRUDSession
import os
from datetime import datetime, timedelta
from core import logger
from pytz import timezone
import json

logging = logger(__name__)


def get_session_token(session_parameter: str):
    try:
        logging.info("Calling get_session_token helper function")
        gateway_url = os.environ["gateway_url"]
        client_id = str(os.environ["client_id"])
        client_secret = str(os.environ["client_secret"])
        session_url = f"{gateway_url}/v0.5/sessions"
        session_obj = CRUDSession().read(session_parameter=session_parameter)
        # logging.info(f"{session_obj=}")
        time_now = datetime.now()
        logging.info(f"{time_now=}")
        ist_tz = timezone("Asia/Kolkata")
        time_now_tz = datetime.now(ist_tz)
        logging.info(f"{time_now_tz=}")
        if session_obj:
            valid_till = session_obj.get("valid_till")
            valid_till_tz = ist_tz.localize(valid_till)
            logging.info(f"{valid_till=}")
            logging.info(f"{valid_till_tz=}")
            if time_now_tz > valid_till_tz:
                logging.info(f"Token expired, generating new access Token")
                resp_json, resp_code = APIInterface().post(
                    route=session_url,
                    data=json.dumps(
                        {"clientId": client_id, "clientSecret": client_secret}
                    ),
                    headers={"Content-Type": "application/json"},
                )
                new_valid_till = time_now_tz + timedelta(
                    seconds=resp_json.get("expiresIn")
                )
                logging.info(f"{new_valid_till=}")
                new_valid_till = new_valid_till.strftime("%Y-%m-%d %H:%M:%S.%f")
                logging.info(f"{new_valid_till=}")
                logging.info(f"Updating database with new generated token")
                CRUDSession().update(
                    **{
                        "parameter": session_parameter,
                        "value": resp_json.get("accessToken"),
                        "expires_in": resp_json.get("expiresIn"),
                        "valid_till": new_valid_till,
                    }
                )
                logging.info("Returning generated accessToken")
                return {"accessToken": resp_json.get("accessToken")}
            else:
                logging.info("Returning existing accessToken")
                return {"accessToken": session_obj.get("value")}
        else:
            logging.info("No session data available, generating access Token")
            resp_json, resp_code = APIInterface().post(
                route=session_url,
                data=json.dumps({"clientId": client_id, "clientSecret": client_secret}),
                headers={"Content-Type": "application/json"},
            )
            if int(resp_code) == 200:
                new_valid_till = time_now_tz + timedelta(
                    seconds=resp_json.get("expiresIn")
                )
                logging.info(f"{new_valid_till=}")
                new_valid_till = new_valid_till.strftime("%Y-%m-%d %H:%M:%S.%f")
                logging.info(f"{new_valid_till=}")
                logging.info(f"Creating new database record for generated token")
                CRUDSession().create(
                    **{
                        "parameter": session_parameter,
                        "type": resp_json.get("tokenType"),
                        "value": resp_json.get("accessToken"),
                        "expires_in": resp_json.get("expiresIn"),
                        "valid_till": new_valid_till,
                    }
                )
                logging.info("Returning generated accessToken")
                return {"accessToken": resp_json.get("accessToken")}
            return {"accessToken": None}
    except Exception as error:
        logging.error(f"Error in get_session_token function: {error}")
        raise error
