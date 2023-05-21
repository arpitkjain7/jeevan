from core.utils.custom.encryption_helper import (
    encrypt_data,
    getEcdhKeyMaterial,
    generateChecksum,
)
from core.utils.custom.external_call import APIInterface
from datetime import datetime, timezone, timedelta
from core.utils.custom.session_helper import get_session_token
import os
import uuid
from pytz import timezone as pytz_timezone


def prepare_data(care_context: dict):
    return {
        "resourceType": "Bundle",
        "id": "bundle01",
        "meta": {"versionId": "1", "lastUpdated": "2020-01-01T15:32:26.605+05:30"},
        "timestamp": "2020-01-01T15:32:26.605+05:30",
        "identifier": {
            "system": "https://example.hospital.com/pr",
            "value": "bundle01",
        },
        "type": "document",
        "entry": [
            {
                "fullUrl": "Composition/1",
                "resource": {
                    "resourceType": "Composition",
                    "id": "1",
                    "date": "2020-01-01T15:32:26.605+05:30",
                    "meta": {
                        "versionId": "1",
                        "lastUpdated": "2020-01-01T15:32:26.605+05:30",
                    },
                    "identifier": {
                        "system": "https://example.hospital.com/documents",
                        "value": "645bb0c3-ff7e-4123-bef5-3852a4784813",
                    },
                    "status": "final",
                    "type": {
                        "coding": [
                            {
                                "system": "https://ndhm.gov.in/sct",
                                "code": "440545006",
                                "display": "Prescription record",
                            }
                        ],
                        "text": "Prescription Record",
                    },
                    "subject": {"reference": "Patient/1", "display": "Hina Patel"},
                    "author": [
                        {"reference": "Practitioner/1", "display": "Dr. Manju Sengar"}
                    ],
                    "title": "Prescription record",
                    "encounter": {
                        "reference": "Encounter/7fce6ec8-5013-4a27-b0a6-c43232608cda",
                        "display": "OP Visit",
                    },
                    "attester": [
                        {
                            "mode": "official",
                            "time": "2019-01-04T09:10:14Z",
                            "party": {
                                "reference": "Organization/MaxSaket01",
                                "display": "Max Super Speciality Hospital, Saket",
                            },
                        }
                    ],
                    "section": [
                        {
                            "title": "Prescription record",
                            "code": {
                                "coding": [
                                    {
                                        "system": "https://affinitydomain.in/sct",
                                        "code": "440545006",
                                        "display": "Prescription record",
                                    }
                                ]
                            },
                            "entry": [{"reference": "MedicationRequest/1"}],
                        }
                    ],
                },
            },
            {
                "fullUrl": "Organization/MaxSaket01",
                "resource": {
                    "resourceType": "Organization",
                    "id": "MaxSaket01",
                    "name": "Max Super Speciality Hospital, Saket",
                    "identifier": [
                        {
                            "type": {
                                "coding": [
                                    {
                                        "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                        "code": "PRN",
                                        "display": "Provider number",
                                    }
                                ]
                            },
                            "system": "https://facility.ndhm.gov.in",
                            "value": "10000005",
                        }
                    ],
                    "address": [
                        {
                            "line": [
                                "1, 2, Press Enclave Marg, Saket Institutional Area, Saket"
                            ],
                            "city": "New Delhi",
                            "state": "New Delhi",
                            "postalCode": "110017",
                            "country": "INDIA",
                        }
                    ],
                },
            },
            {
                "fullUrl": "Encounter/7fce6ec8-5013-4a27-b0a6-c43232608cda",
                "resource": {
                    "resourceType": "Encounter",
                    "id": "7fce6ec8-5013-4a27-b0a6-c43232608cda",
                    "status": "finished",
                    "class": {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                        "code": "AMB",
                        "display": "Outpatient visit",
                    },
                },
            },
            {
                "fullUrl": "MedicationRequest/1",
                "resource": {
                    "id": "1",
                    "resourceType": "MedicationRequest",
                },
            },
        ],
    }


def send_data(hi_request: dict, consent_obj: dict, transaction_id: str):
    data_push_url = hi_request.get("dataPushUrl")
    key_material = hi_request.get("keyMaterial")
    consent_data = consent_obj.get("callback_response")
    hip_id = consent_data.get("hip").get("id")
    care_context_list = consent_data.get("careContexts")
    care_context_output, care_context_ack = [], []
    sender_key_material = getEcdhKeyMaterial()
    for care_context_obj in care_context_list:
        fhir_bundle = prepare_data(care_context=care_context_obj)
        checksum = generateChecksum(json_data=fhir_bundle)
        encryption_obj = encrypt_data(
            stringToEncrypt=f"{fhir_bundle}",
            requesterKeyMaterial=key_material,
            senderKeyMaterial=sender_key_material,
        )
        encrypted_data = encryption_obj.get("encryptedData")
        care_context_output.append(
            {
                "content": encrypted_data,
                "media": "application/fhir+json",
                "checksum": checksum,
                "careContextReference": care_context_obj.get("careContextReference"),
            }
        )
        care_context_ack.append(
            {
                "careContextReference": care_context_obj.get("careContextReference"),
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
    _, resp_code = APIInterface().post(route=data_push_url, data=data_request)
    request_id = str(uuid.uuid1())
    time_now = datetime.now(timezone.utc)
    time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
    gateway_access_token = get_session_token(session_parameter="gateway_token").get(
        "accessToken"
    )
    gateway_url = os.environ["gateway_url"]
    data_transfer_success_url = f"{gateway_url}/v0.5/health-information/notify"
    request = {
        "requestId": request_id,
        "timestamp": time_now,
        "notification": {
            "consentId": consent_obj.get("request_id"),
            "transactionId": transaction_id,
            "doneAt": time_now,
            "notifier": {"type": "HIP", "id": hip_id},
            "statusNotification": {
                "sessionStatus": "TRANSFERRED",
                "hipId": hip_id,
                "statusResponses": care_context_ack,
            },
        },
    }
    headers = (
        {
            "X-CM-ID": "sbx",
            "Authorization": f"Bearer {gateway_access_token}",
        },
    )
    _, ack_resp_code = APIInterface().post(
        route=data_transfer_success_url, data=request, headers=headers
    )
