from core.utils.custom.encryption_helper import (
    encrypt_data,
    getEcdhKeyMaterial,
    generateChecksum,
)
from core.utils.custom.external_call import APIInterface
from datetime import datetime, timezone, timedelta
from core.utils.custom.session_helper import get_session_token
from core.crud.hrp_gatewayInteraction_crud import CRUDGatewayInteraction
import os
import uuid
from pytz import timezone as pytz_timezone
from core import logger
from core import celery
import base64

logging = logger(__name__)


def prepare_data(care_context, file_bytes):
    logging.info("Preparing data to transfer")
    return {
        "resourceType": "Bundle",
        "id": "9473cf69-9fb8-4551-908f-94d0e081b9cc",
        "type": "document",
        "entry": [
            {
                "fullUrl": "Composition/1007DR1",
                "resource": {
                    "resourceType": "Composition",
                    "id": "1007DR1",
                    "date": "2019-01-03T15:32:26.605+05:30",
                    "text": {"status": "generated"},
                    "identifier": {
                        "system": "https://www.max.in/composition",
                        "value": "1007DR1",
                    },
                    "status": "final",
                    "type": {
                        "coding": [
                            {
                                "system": "https://ndhm.gov.in/sct",
                                "code": "721981007",
                                "display": "Diagnostic Report",
                            }
                        ],
                        "text": "Prescription record",
                    },
                    "encounter": {
                        "reference": "Encounter/7fce6ec8-5013-4a27-b0a6-c43232608cda",
                        "display": "OPD Visit - patient walked in",
                    },
                    "subject": {"reference": "Patient/RVH1002"},
                    "author": [
                        {"reference": "Organization/MaxSaket01"},
                        {"reference": "Practitioner/DHID1234"},
                    ],
                    "title": "Doc: Surgical Pathology Report",
                    "section": [
                        {
                            "title": "Diagnostic report: CBC",
                            "code": {
                                "coding": [
                                    {
                                        "system": "https://ndhm.gov.in/sct",
                                        "code": "721981007",
                                        "display": "Diagnosti Report: Complete Blood Count",
                                    }
                                ]
                            },
                            "entry": [
                                {
                                    "reference": "DiagnosticReport/a45840dc-cf6b-4fcc-acec-d54a3bea40ff"
                                }
                            ],
                        }
                    ],
                },
            },
            {
                "fullUrl": "DiagnosticReport/a45840dc-cf6b-4fcc-acec-d54a3bea40ff",
                "resource": {
                    "resourceType": "DiagnosticReport",
                    "id": "a45840dc-cf6b-4fcc-acec-d54a3bea40ff",
                    "status": "final",
                    "code": {"text": "Complete Blood Count Panel"},
                    "effectiveDateTime": "2019-11-03T00:00:00+00:00",
                    "issued": "2019-11-05T00:00:00+00:00",
                    "presentedForm": [
                        {
                            "contentType": "application/pdf",
                            "data": f"{file_bytes}",
                            "title": "Complete Blood Count (CBC)",
                        }
                    ],
                },
            },
        ],
    }
    # return {
    #     "resourceType": "Bundle",
    #     "id": "3739707e-1123-46fe-918f-b52d880e4e7f",
    #     "meta": {"lastUpdated": "2016-08-07T00:00:00.000+05:30"},
    #     "identifier": {
    #         "system": "https://www.max.in/bundle",
    #         "value": "3739707e-1123-46fe-918f-b52d880e4e7f",
    #     },
    #     "type": "document",
    #     "timestamp": "2016-08-07T00:00:00.000+05:30",
    #     "entry": [
    #         {
    #             "fullUrl": "Composition/c63d1435-b6b6-46c4-8163-33133bf0d9bf",
    #             "resource": {
    #                 "resourceType": "Composition",
    #                 "id": "c63d1435-b6b6-46c4-8163-33133bf0d9bf",
    #                 "identifier": {
    #                     "system": "https://www.max.in/document",
    #                     "value": "c63d1435-b6b6-46c4-8163-33133bf0d9bf",
    #                 },
    #                 "status": "final",
    #                 "type": {
    #                     "coding": [
    #                         {
    #                             "system": "https://projecteka.in/sct",
    #                             "code": "440545006",
    #                             "display": "Prescription record",
    #                         }
    #                     ]
    #                 },
    #                 "subject": {"reference": "Patient/RVH9999"},
    #                 "encounter": {
    #                     "reference": "Encounter/dab7fd2b-6a05-4adb-af35-bcffd6c85b81"
    #                 },
    #                 "date": "2016-08-07T00:00:00.605+05:30",
    #                 "author": [
    #                     {
    #                         "reference": "Practitioner/MAX5001",
    #                         "display": "Dr Laxmikanth J",
    #                     }
    #                 ],
    #                 "title": "Prescription",
    #                 "section": [
    #                     {
    #                         "title": "OPD Prescription",
    #                         "code": {
    #                             "coding": [
    #                                 {
    #                                     "system": "https://projecteka.in/sct",
    #                                     "code": "440545006",
    #                                     "display": "Prescription record",
    #                                 }
    #                             ]
    #                         },
    #                         "entry": [
    #                             {
    #                                 "reference": "MedicationRequest/68d9667c-00c3-455f-b75d-d580950498a0"
    #                             }
    #                         ],
    #                     }
    #                 ],
    #             },
    #         },
    #         {
    #             "fullUrl": "Practitioner/MAX5001",
    #             "resource": {
    #                 "resourceType": "Practitioner",
    #                 "id": "MAX5001",
    #                 "identifier": [
    #                     {"system": "https://www.mciindia.in/doctor", "value": "MAX5001"}
    #                 ],
    #                 "name": [
    #                     {"text": "Laxmikanth J", "prefix": ["Dr"], "suffix": ["MD"]}
    #                 ],
    #             },
    #         },
    #         {
    #             "fullUrl": "Patient/RVH9999",
    #             "resource": {
    #                 "resourceType": "Patient",
    #                 "id": "RVH9999",
    #                 "name": [{"text": "Keith David"}],
    #                 "gender": "male",
    #             },
    #         },
    #         {
    #             "fullUrl": "Encounter/dab7fd2b-6a05-4adb-af35-bcffd6c85b81",
    #             "resource": {
    #                 "resourceType": "Encounter",
    #                 "id": "dab7fd2b-6a05-4adb-af35-bcffd6c85b81",
    #                 "status": "finished",
    #                 "class": {
    #                     "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
    #                     "code": "AMB",
    #                     "display": "Outpatient visit",
    #                 },
    #                 "subject": {"reference": "Patient/RVH9999"},
    #                 "period": {"start": "2016-08-07T00:00:00+05:30"},
    #             },
    #         },
    #         {
    #             "fullUrl": "Medication/54ab5657-5e79-4461-a823-20e522eb337d",
    #             "resource": {
    #                 "resourceType": "Medication",
    #                 "id": "54ab5657-5e79-4461-a823-20e522eb337d",
    #                 "code": {
    #                     "coding": [
    #                         {
    #                             "system": "https://projecteka.in/act",
    #                             "code": "R05CB02",
    #                             "display": "bromhexine 24 mg",
    #                         }
    #                     ]
    #                 },
    #             },
    #         },
    #         {
    #             "fullUrl": "MedicationRequest/68d9667c-00c3-455f-b75d-d580950498a0",
    #             "resource": {
    #                 "resourceType": "MedicationRequest",
    #                 "id": "68d9667c-00c3-455f-b75d-d580950498a0",
    #                 "status": "active",
    #                 "intent": "order",
    #                 "medicationReference": {
    #                     "reference": "Medication/54ab5657-5e79-4461-a823-20e522eb337d"
    #                 },
    #                 "subject": {"reference": "Patient/RVH9999"},
    #                 "authoredOn": "2016-08-07T00:00:00+05:30",
    #                 "requester": {"reference": "Practitioner/MAX5001"},
    #                 "dosageInstruction": [{"text": "1 capsule 2 times a day"}],
    #             },
    #         },
    #     ],
    # }
    # return {
    #     "resourceType": "Bundle",
    #     "id": "bundle01",
    #     "meta": {"versionId": "1", "lastUpdated": "2020-01-01T15:32:26.605+05:30"},
    #     "timestamp": "2020-01-01T15:32:26.605+05:30",
    #     "identifier": {
    #         "system": "https://example.hospital.com/pr",
    #         "value": "bundle01",
    #     },
    #     "type": "document",
    #     "entry": [
    #         {
    #             "fullUrl": "Composition/1",
    #             "resource": {
    #                 "resourceType": "Composition",
    #                 "id": "1",
    #                 "date": "2020-01-01T15:32:26.605+05:30",
    #                 "meta": {
    #                     "versionId": "1",
    #                     "lastUpdated": "2020-01-01T15:32:26.605+05:30",
    #                 },
    #                 "identifier": {
    #                     "system": "https://example.hospital.com/documents",
    #                     "value": "645bb0c3-ff7e-4123-bef5-3852a4784813",
    #                 },
    #                 "status": "final",
    #                 "type": {
    #                     "coding": [
    #                         {
    #                             "system": "https://ndhm.gov.in/sct",
    #                             "code": "440545006",
    #                             "display": "Prescription record",
    #                         }
    #                     ],
    #                     "text": "Prescription Record",
    #                 },
    #                 "subject": {"reference": "Patient/1", "display": "Hina Patel"},
    #                 "author": [
    #                     {"reference": "Practitioner/1", "display": "Dr. Manju Sengar"}
    #                 ],
    #                 "title": "Prescription record",
    #                 "encounter": {
    #                     "reference": "Encounter/7fce6ec8-5013-4a27-b0a6-c43232608cda",
    #                     "display": "OP Visit",
    #                 },
    #                 "attester": [
    #                     {
    #                         "mode": "official",
    #                         "time": "2019-01-04T09:10:14Z",
    #                         "party": {
    #                             "reference": "Organization/MaxSaket01",
    #                             "display": "Max Super Speciality Hospital, Saket",
    #                         },
    #                     }
    #                 ],
    #                 "section": [
    #                     {
    #                         "title": "Prescription record",
    #                         "code": {
    #                             "coding": [
    #                                 {
    #                                     "system": "https://affinitydomain.in/sct",
    #                                     "code": "440545006",
    #                                     "display": "Prescription record",
    #                                 }
    #                             ]
    #                         },
    #                         "entry": [{"reference": "MedicationRequest/1"}],
    #                     }
    #                 ],
    #             },
    #         },
    #         {
    #             "fullUrl": "Organization/MaxSaket01",
    #             "resource": {
    #                 "resourceType": "Organization",
    #                 "id": "MaxSaket01",
    #                 "name": "Max Super Speciality Hospital, Saket",
    #                 "identifier": [
    #                     {
    #                         "type": {
    #                             "coding": [
    #                                 {
    #                                     "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
    #                                     "code": "PRN",
    #                                     "display": "Provider number",
    #                                 }
    #                             ]
    #                         },
    #                         "system": "https://facility.ndhm.gov.in",
    #                         "value": "10000005",
    #                     }
    #                 ],
    #                 "address": [
    #                     {
    #                         "line": [
    #                             "1, 2, Press Enclave Marg, Saket Institutional Area, Saket"
    #                         ],
    #                         "city": "New Delhi",
    #                         "state": "New Delhi",
    #                         "postalCode": "110017",
    #                         "country": "INDIA",
    #                     }
    #                 ],
    #             },
    #         },
    #         {
    #             "fullUrl": "Encounter/7fce6ec8-5013-4a27-b0a6-c43232608cda",
    #             "resource": {
    #                 "resourceType": "Encounter",
    #                 "id": "7fce6ec8-5013-4a27-b0a6-c43232608cda",
    #                 "status": "finished",
    #                 "class": {
    #                     "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
    #                     "code": "AMB",
    #                     "display": "Outpatient visit",
    #                 },
    #             },
    #         },
    #         {
    #             "fullUrl": "MedicationRequest/1",
    #             "resource": {
    #                 "id": "1",
    #                 "resourceType": "MedicationRequest",
    #             },
    #         },
    #     ],
    # }


# def process_task(customer_name):
#     try:
#         logging.info("executing  process_task function")
#         return {"message": "Order Received! Thank you for your patience."}
#     except Exception as error:
#         logging.error(f"Error in process_task function: {error}")
#         raise error


@celery.task
def send_data_copy(
    hi_request: dict, consent_id: str, transaction_id: str, request_id: str
):
    logging.info("send_data_copy triggered")
    logging.info(f"{hi_request=},{consent_id=},{transaction_id=},{request_id=}")
    logging.info("FINISHED")


@celery.task
def send_data_copy_1(customer_name, order_quantity):
    logging.info("send_data_copy_1 triggered")
    logging.info(f"{customer_name=},{order_quantity=}")
    logging.info("FINISHED")


def send_data(
    hi_request: dict, consent_obj: dict, transaction_id: str, request_id: str
):
    try:
        logging.info("send_data triggered")
        logging.info(f"{hi_request=}")
        data_push_url = hi_request.get("dataPushUrl")
        key_material = hi_request.get("keyMaterial")
        consent_data = consent_obj.get("care_contexts")
        hip_id = consent_obj.get("hip_id")
        care_context_list = consent_data.get("care_context")
        care_context_output, care_context_ack = [], []
        sender_key_material = getEcdhKeyMaterial()
        for care_context_obj in care_context_list:
            logging.info(f"{care_context_obj=}")
            with open("/app/core/utils/custom/testimage.png", "rb") as pdf_file:
                # encoded_string = base64.b64encode(pdf_file.read())
                encoded_string = pdf_file.read()
            fhir_bundle = prepare_data(
                care_context=care_context_obj, file_bytes=encoded_string
            )
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
                    "careContextReference": care_context_obj.get(
                        "careContextReference"
                    ),
                }
            )
            care_context_ack.append(
                {
                    "careContextReference": care_context_obj.get(
                        "careContextReference"
                    ),
                    "hiStatus": "OK",
                    "description": "Transfered Successfully",
                }
            )
        logging.info(f"{care_context_output=}")
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
        logging.info(f"Data push {resp_code=}")
        ack_request_id = str(uuid.uuid1())
        time_now = datetime.now(timezone.utc)
        time_now = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")
        gateway_access_token = get_session_token(session_parameter="gateway_token").get(
            "accessToken"
        )
        gateway_url = os.environ["gateway_url"]
        data_transfer_success_url = f"{gateway_url}/v0.5/health-information/notify"
        request = {
            "requestId": ack_request_id,
            "timestamp": time_now,
            "notification": {
                "consentId": consent_obj.get("id"),
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
        headers = {"X-CM-ID": "sbx", "Authorization": f"Bearer {gateway_access_token}"}
        _, ack_resp_code = APIInterface().post(
            route=data_transfer_success_url, data=request, headers=headers
        )
        logging.info(f"ack sent {ack_resp_code=}")
        gateway_request = {"request_id": request_id}
        if ack_resp_code <= 250:
            gateway_request.update({"request_status": "SUCCESS"})
        else:
            gateway_request.update({"request_status": "FAILED"})
        CRUDGatewayInteraction().update(**gateway_request)
        return gateway_request
    except Exception as error:
        logging.error(f"Error in send_data function: {error}")
        raise error
