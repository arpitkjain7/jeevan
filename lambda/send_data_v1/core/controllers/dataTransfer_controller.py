from core.utils.custom.external_call import APIInterface
from pytz import timezone as pytz_timezone
from dateutil import parser
from core.utils.aws.s3_helper import read_json
from core.utils.custom.encryption_helper import (
    encrypt_data,
    generateChecksum,
    getEcdhKeyMaterial,
    decryptData,
)
from datetime import datetime, timedelta
import os, json
import ast


class DataTransferController:
    def __init__(self):
        self.callback_base_url = os.environ["callback_base_url"]

    def send_data(self, data_obj: dict, request_type: str):
        try:
            print(f"{data_obj=}")
            transaction_id = data_obj.get("transaction_id")
            if request_type == "encrypt":
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
                        print(f"{checksum=}")
                        encryption_obj = encrypt_data(
                            stringToEncrypt=f"{fhir_bundle}",
                            requesterKeyMaterial=receiver_key_material,
                            senderKeyMaterial=sender_key_material,
                        )
                        print(f"{encryption_obj=}")
                        encrypted_data = encryption_obj.get("encryptedData")
                        print(f"{encrypted_data=}")
                        care_context_output.append(
                            {
                                "content": encrypted_data,
                                "media": "application/fhir+json",
                                "checksum": checksum,
                                "careContextReference": care_context_ref,
                            }
                        )
                        print(f"{care_context_output=}")
                        care_context_ack.append(
                            {
                                "careContextReference": care_context_ref,
                                "hiStatus": "OK",
                                "description": "Transfered Successfully",
                            }
                        )
                        print(f"{care_context_ack=}")
                expiry_datetime = datetime.utcnow() + timedelta(days=1)
                expiry_datetime = expiry_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                data_request = {
                    "pageNumber": 0,
                    "pageCount": 1,
                    "transactionId": transaction_id,
                    "entries": care_context_output,
                    "keyMaterial": {
                        "cryptoAlg": "ECDH",
                        "curve": "Curve25519",
                        "dhPublicKey": {
                            "expiry": expiry_datetime,
                            "parameters": "Curve25519/32byte random key",
                            "keyValue": sender_key_material.get("x509PublicKey"),
                        },
                        "nonce": sender_key_material.get("nonce"),
                    },
                }
                print(f"{data_request=}")
                resp, resp_code = APIInterface().post(
                    route=data_push_url, data=data_request
                )
                print(f"Data push {resp_code=}")
                print(f"Data push {resp=}")
                ack_data_request = {
                    "consent_id": consent_id,
                    "transaction_id": transaction_id,
                    "hip_id": hip_id,
                    "care_context_ack": care_context_ack,
                    "request_id": request_id,
                }
                ack_resp, ack_resp_code = APIInterface().post(
                    route=f"{self.callback_base_url}/v1/data_transfer_ack",
                    data=ack_data_request,
                )
                return {
                    "data_push_status": {
                        "response_code": resp_code,
                        "response_txt": resp,
                    },
                    "ack_status": {
                        "response_code": ack_resp_code,
                        "response_txt": ack_resp,
                    },
                }
            elif request_type == "decrypt":
                patient_data_list = []
                resources_dict = {}
                patient_data_transformed = []
                transaction_id = data_obj.get("transactionId")
                patient_data = data_obj.get("entries")
                requesterNonce = data_obj.get("requesterNonce")
                senderNonce = data_obj.get("senderNonce")
                requesterPrivateKey = data_obj.get("requesterPrivateKey")
                senderPublicKey = data_obj.get("senderPublicKey")
                for entry in patient_data:
                    encrypted_data = entry.get("content")
                    decrypted_data = decryptData(
                        decryptParams={
                            "encryptedData": encrypted_data,
                            "requesterNonce": requesterNonce,
                            "senderNonce": senderNonce,
                            "requesterPrivateKey": requesterPrivateKey,
                            "senderPublicKey": senderPublicKey,
                        }
                    )
                    decrypted_json = json.loads(decrypted_data)
                    fhir_data = decrypted_json.get("decryptedData")
                    fhir_json = ast.literal_eval(fhir_data)
                    data_entries = fhir_json["entry"]
                    for entry in data_entries:
                        resources_dict[entry["resource"]["resourceType"]] = entry[
                            "resource"
                        ]
                    patient_data_transformed.append(resources_dict)
                    patient_data_list.append(fhir_json)
                print(f"{patient_data_list=}")
                callback_payload = {
                    "id": consent_id,
                    "patient_data_list": patient_data_list,
                    "patient_data_transformed": patient_data_transformed,
                }
                print(f"{callback_payload=}")

                resp, resp_code = APIInterface().post(
                    route=f"{self.callback_base_url}/v1/HIU/storeData",
                    data=callback_payload,
                )
                print(f"{resp=} || {resp_code=}")
        except Exception as error:
            print(f"Error in DataTransferController.data_request function: {error}")
            raise error
