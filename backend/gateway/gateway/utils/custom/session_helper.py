from gateway.utils.custom.external_call import APIInterface
from gateway.crud.hrp_session_crud import CRUDSession
import os
from datetime import datetime, timedelta
from gateway import logger

logging = logger(__name__)


def get_session_token(session_parameter: str):
    try:
        logging.info("Calling get_session_token helper function")
        gateway_url = os.environ["gateway_url"]
        client_id = os.environ["client_id"]
        client_secret = os.environ["client_secret"]
        session_url = f"{gateway_url}/v0.5/sessions"
        session_obj = CRUDSession().read(session_parameter=session_parameter)
        logging.info(f"{session_obj=}")
        time_now = datetime.now()
        if session_obj:
            valid_till = session_obj.get("valid_till")
            if time_now > valid_till:
                logging.info(f"Token expired, generating new access Token")
                resp_json, _ = APIInterface().post(
                    route=session_url,
                    data={"clientId": client_id, "clientSecret": client_secret},
                )
                new_valid_till = time_now + timedelta(
                    seconds=resp_json.get("expiresIn")
                )
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
            resp_json, _ = APIInterface().post(
                route=session_url,
                data={"clientId": client_id, "clientSecret": client_secret},
            )
            new_valid_till = time_now + timedelta(seconds=resp_json.get("expiresIn"))
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
    except Exception as error:
        logging.error(f"Error in get_session_token function: {error}")
        raise error
