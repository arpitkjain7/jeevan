from core.utils.custom.external_call import APIInterface
import os
import uuid
from pytz import timezone as pytz_timezone
from dateutil import parser
from core.utils.custom.encryption_helper import (
    encrypt_data,
    generateChecksum,
    getEcdhKeyMaterial,
)
import os


class DataTransferController:
    def __init__(self):
        self.base_url = os.environ["base_url"]
        self.endpoint = os.environ["ack_endpoint"]

    def data_request(self, data_obj: dict):
        try:
            print(f"{data_obj=}")
            transaction_id = data_obj.get("transaction_id")
            request_id = data_obj.get("request_id")
            hip_id = data_obj.get("hip_id")
            consent_id = data_obj.get("consent_id")
            data_push_url = data_obj.get("data_push_url")
            receiver_key_material = data_obj.get("receiver_key_material")
            fhir_bundles = data_obj.get("fhir_bundles")
            sender_key_material = getEcdhKeyMaterial()
            print(f"{sender_key_material=}")
            care_context_output, care_context_ack = [], []
            for fhir_obj in fhir_bundles:
                print(f"{fhir_obj=}")
                for care_context_ref, fhir_bundle in fhir_obj.items():
                    print(f"{care_context_ref=}")
                    checksum = generateChecksum(json_data=fhir_bundle)
                    encryption_obj = encrypt_data(
                        stringToEncrypt=f"{fhir_bundle}",
                        requesterKeyMaterial=receiver_key_material,
                        senderKeyMaterial=sender_key_material,
                    )
                    encrypted_data = encryption_obj.get("encryptedData")
                    care_context_output.append(
                        {
                            "content": encrypted_data,
                            "media": "application/fhir+json",
                            "checksum": checksum,
                            "careContextReference": care_context_ref,
                        }
                    )
                    care_context_ack.append(
                        {
                            "careContextReference": care_context_ref,
                            "hiStatus": "OK",
                            "description": "Transfered Successfully",
                        }
                    )
            data_request = {
                "pageNumber": 0,
                "pageCount": 1,
                "transactionId": transaction_id,
                "entries": care_context_output,
                "keyMaterial": {
                    "cryptoAlg": "ECDH",
                    "curve": "Curve25519",
                    "dhPublicKey": {
                        "expiry": "2024-10-06T10:50:37.764Z",
                        "parameters": "Curve25519/32byte random key",
                        "keyValue": sender_key_material.get("x509PublicKey"),
                    },
                    "nonce": sender_key_material.get("nonce"),
                },
            }
            resp, resp_code = APIInterface().post(
                route=data_push_url, data=data_request
            )
            print(f"Data push {resp_code=}")
            ack_data_request = {
                "consent_id": consent_id,
                "transaction_id": transaction_id,
                "hip_id": hip_id,
                "care_context_ack": care_context_ack,
                "request_id": request_id,
            }
            ack_resp, ack_resp_code = APIInterface().post(
                route=f"{self.base_url}{self.endpoint}", data=ack_data_request
            )
            return {
                "data_push_status": {"response_code": resp_code, "response_txt": resp},
                "ack_status": {
                    "response_code": ack_resp_code,
                    "response_txt": ack_resp,
                },
            }
        except Exception as error:
            print(f"Error in DataTransferController.data_request function: {error}")
            raise error
