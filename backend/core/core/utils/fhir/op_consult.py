# from core import logger
from datetime import datetime, timezone
from fhir.resources.bundle import Bundle, BundleEntry
from fhir.resources.meta import Meta
from fhir.resources.identifier import Identifier
import pytz
import uuid
from core.utils.fhir.modules import *
from core.crud.hims_patientMedicalRecord_crud import CRUDPatientMedicalRecord
from core.crud.hims_slots_crud import CRUDSlots
from core.crud.hims_patientMedicalDocuments_crud import CRUDPatientMedicalDocuments
from core.crud.hims_hip_crud import CRUDHIP
from core.crud.hims_appointments_crud import CRUDAppointments
from core.crud.hims_patientDetails_crud import CRUDPatientDetails
from core.crud.hims_docDetails_crud import CRUDDocDetails
from core.crud.hims_symptoms_crud import CRUDSymptoms
from core.crud.hims_vitals_crud import CRUDVital
from core.crud.hims_medicalHistory_crud import CRUDMedicalHistory
from core.crud.hims_medicines_crud import CRUDMedicines
from core.utils.aws.s3_helper import get_object, read_object
from core import logger
import json
import uuid
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

logging = logger(__name__)
# logging = logger(__name__)
timezone = pytz.timezone("Asia/Kolkata")


def remove_none_values(d):
    if isinstance(d, dict):
        return {
            key: remove_none_values(value)
            for key, value in d.items()
            if value is not None
        }
    elif isinstance(d, list):
        return [remove_none_values(item) for item in d if item is not None]
    else:
        return d


def opConsultUnstructured(bundle_name: str, bundle_identifier: str, pmr_id: str):
    logging.info("executing opConsultUnstructured function")
    time_str = datetime.now(timezone).isoformat()
    logging.info(f"Getting PMR record")
    pmr_obj = CRUDPatientMedicalRecord().read(pmr_id=pmr_id)
    if pmr_obj:
        logging.info(f"Getting Doctor record")
        doc_rec = CRUDDocDetails().read_by_docId(doc_id=pmr_obj["doc_id"])
        logging.info(f"Getting Appointment record")
        appointment_rec = CRUDAppointments().read(
            appointment_id=pmr_obj["appointment_id"]
        )
        logging.info(f"Getting HIP record")
        hip_rec = CRUDHIP().read(hip_ip=pmr_obj["hip_id"])
        logging.info(f"Getting Patient record")
        patient_rec = CRUDPatientDetails().read_by_patientId(
            patient_id=pmr_obj["patient_id"]
        )
        pmr_obj.update(
            {
                "hip": hip_rec,
                "doctor": doc_rec,
                "appointment": appointment_rec,
                "patient": patient_rec,
            }
        )
        logging.info(f"{pmr_obj=}")
        # pmr_obj = CRUDPatientMedicalRecord().read_details(pmr_id=pmr_id)
        composition_section_list, entry_list = [], []
        doctor_obj = pmr_obj.get("doctor")
        logging.info(f"{doctor_obj=}")
        # doctor_id = pmr_obj.get("doc_id")
        # doc_obj = CRUDDocDetails().read_by_docId(doc_id=doctor_id)
        practitioner_bundle = BundleEntry()
        practitioner_url = f"Practitioner/{doctor_obj['id']}"
        practitioner_bundle.fullUrl = practitioner_url
        practitioner_bundle.resource = practitioner(
            practitioner_id=doctor_obj["id"],
            medical_licence_number=doctor_obj["doc_licence_no"],
            practitioner_name=doctor_obj["doc_name"],
        )
        entry_list.append(practitioner_bundle)
        # Creating Organization Entry
        # hip_id = pmr_obj.get("hip_id")
        # hip_obj = CRUDHIP().read(hip_ip=hip_id)
        logging.info(f"Creating Organization Entry")
        hip_obj = pmr_obj.get("hip")
        logging.info(f"{hip_obj=}")
        organization_bundle = BundleEntry()
        organization_url = f"Organization/{hip_obj['id']}"
        organization_bundle.fullUrl = organization_url
        organization_bundle.resource = organization(
            organization_id=hip_obj["id"],
            organization_name=hip_obj["name"],
            organization_prn=hip_obj["hfr_reg_number"],
            organization_email_id=hip_obj["hip_email_address"],
            organization_phone_number=hip_obj["hip_contact_number"],
        )
        entry_list.append(organization_bundle)
        # Creating Patient Entry
        # patient_id = pmr_obj.get("patient_id")
        # patient_obj = CRUDPatientDetails().read_by_patientId(patient_id=patient_id)
        logging.info(f"Creating Patient Entry")
        patient_obj = pmr_obj.get("patient")
        logging.info(f"{patient_obj=}")
        birth_year, birth_month, birth_date = patient_obj["DOB"].split("-")
        patient_bundle = BundleEntry()
        patient_url = f"Patient/{patient_obj['id']}"
        patient_bundle.fullUrl = patient_url
        patient_bundle.resource = patient(
            patient_id=patient_obj["id"],
            patient_mobile_number=patient_obj["mobile_number"],
            patient_dob=f"{birth_year}-{birth_date}-{birth_month}",
            patient_gender=patient_obj["gender"],
            patient_abha_id=patient_obj["abha_number"],
            patient_name=patient_obj["name"],
        )
        entry_list.append(patient_bundle)
        # Creating Encounter Entry
        logging.info(f"Creating Encounter Entry")
        appointment_obj = pmr_obj.get("appointment")
        logging.info(f"{appointment_obj=}")
        slot_id = appointment_obj.get("slot_id")
        slot_obj = CRUDSlots().read(slot_id=slot_id)
        logging.info(f"{slot_obj=}")
        encounter_start = datetime.combine(slot_obj["date"], slot_obj["start_time"])
        encounter_end = datetime.combine(slot_obj["date"], slot_obj["end_time"])
        encounter_bundle = BundleEntry()
        encounter_url = f"Encounter/{appointment_obj['id']}"
        encounter_bundle.fullUrl = encounter_url
        encounter_bundle.resource = encounter(
            encounter_id=appointment_obj["id"],
            encounter_type_code=appointment_obj["encounter_type_code"],
            encounter_type_display=appointment_obj["encounter_type_code"],
            encounter_start=encounter_start,
            encounter_end=encounter_end,
            patient_reference=patient_url,
        )
        entry_list.append(encounter_bundle)
        # Creating Appointment Entry
        logging.info(f"Creating Appointment Entry")
        appointment_obj = pmr_obj.get("appointment")
        logging.info(f"{appointment_obj=}")
        appointment_bundle = BundleEntry()
        appointment_url = f"Appointment/{appointment_obj['id']}"
        appointment_bundle.fullUrl = appointment_url
        appointment_bundle.resource = appointment(
            patient_ref=patient_url,
            practitioner_ref=practitioner_url,
            status=appointment_obj["consultation_status"],
            start_timestamp=encounter_start,
            end_timestamp=encounter_end,
        )
        entry_list.append(appointment_bundle)
        codeable_obj = CodeableConcept()
        codeable_obj.coding = [
            {
                "system": "http://snomed.info/sct",
                "code": "736271009",
                "display": "Outpatient care plan",
            }
        ]
        composition_section = CompositionSection(
            title="Follow Up",
            code=codeable_obj,
            entry=[{"reference": appointment_url}],
        )
        composition_section_list.append(composition_section)
        # Creating Document Entry
        logging.info(f"Creating Document Entry")
        pmr_document_list = CRUDPatientMedicalDocuments().read_by_pmr_id(pmr_id=pmr_id)
        logging.info(f"{pmr_document_list=}")
        for pmr_document_obj in pmr_document_list:
            document_bundle = BundleEntry()
            document_location = pmr_document_obj.get("document_location")
            bucket_name = document_location.split("/")[0]
            document_key = "/".join(document_location.split("/")[1:])
            document_content = read_object(bucket_name=bucket_name, prefix=document_key)
            document_url = f"DocumentReference/{pmr_document_obj['id']}"
            document_bundle.fullUrl = document_url
            document_bundle.resource = document(
                document_ref_id=pmr_document_obj["id"],
                document_code=pmr_document_obj["document_type_code"],
                document_display_name=pmr_document_obj["document_type"],
                patient_ref=patient_url,
                document_mime_type=pmr_document_obj["document_mime_type"],
                document_bytes=document_content,
            )
            codeable_obj = CodeableConcept()
            codeable_obj.coding = [
                {
                    "system": "http://snomed.info/sct",
                    "code": "371530004",
                    "display": "Clinical consultation report",
                }
            ]
            entry_list.append(document_bundle)
            composition_section = CompositionSection(
                title="Document Reference",
                code=codeable_obj,
                entry=[{"reference": document_url}],
            )
            composition_section_list.append(composition_section)
        # Creating Composition
        logging.info(f"Creating Composition Entry")
        composition_bundle = BundleEntry()
        composition_bundle.fullUrl = f"Composition/1"
        composition_id = str(uuid.uuid1())
        composition_resource_obj = composition(
            composition_id=composition_id,
            composition_profile_id="https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord",
            pmr_id=pmr_id,
            patient_ref=[{"reference": patient_url, "type": "Patient"}],
            doctor_ref=[{"reference": practitioner_url}],
            org_ref={"reference": organization_url},
            encounter_ref={"reference": encounter_url, "type": "Encounter"},
        )

        # composition_section = CompositionSection(
        #     entry=[{"reference": document_url}, {"reference": appointment_url}]
        # )
        composition_resource_obj.section = composition_section_list
        composition_bundle.resource = composition_resource_obj
        entry_list.append(composition_bundle)
        # Creating Bundle
        logging.info(f"Creating Bundle Entry")
        identifier = Identifier()
        identifier.value = bundle_identifier
        meta = Meta(
            versionId=1,
            lastUpdated=time_str,
            profile=[
                "https://nrces.in/ndhm/fhir/r4/StructureDefinition/DocumentBundle"
            ],
            security=[
                {
                    "system": "http://terminology.hl7.org/CodeSystem/v3-Confidentiality",
                    "code": "V",
                    "display": "very restricted",
                }
            ],
        )
        bundle = Bundle(
            id=bundle_name,
            type="document",
            timestamp=time_str,
            identifier=identifier,
            entry=entry_list,
        )
        bundle.meta = meta
        bundle_dict = bundle.__dict__
        bundle_json = JSONResponse(content=jsonable_encoder(bundle_dict))
        content_bytes = bundle_json.body
        content_str = content_bytes.decode("utf-8")
        response_dict = json.loads(content_str)
        response_dict = remove_none_values(response_dict)
        response_dict["resourceType"] = response_dict.pop("resource_type")
        return response_dict
    logging.info(f"No record found for {pmr_id=}")
    return None


def opConsultDummy(bundle_name: str, bundle_identifier: str, pmr_id: str):
    logging.info("executing opConsultDummy function")
    time_str = datetime.now(timezone).isoformat()
    logging.info(f"Getting PMR record")
    pmr_obj = CRUDPatientMedicalRecord().read(pmr_id=pmr_id)
    dummy_fhir = None
    if pmr_obj:
        logging.info(f"Getting Doctor record")
        doc_rec = CRUDDocDetails().read_by_docId(doc_id=pmr_obj["doc_id"])
        logging.info(f"Getting Appointment record")
        appointment_rec = CRUDAppointments().read(
            appointment_id=pmr_obj["appointment_id"]
        )
        logging.info(f"Getting HIP record")
        hip_rec = CRUDHIP().read(hip_ip=pmr_obj["hip_id"])
        logging.info(f"Getting Patient record")
        patient_rec = CRUDPatientDetails().read_by_patientId(
            patient_id=pmr_obj["patient_id"]
        )
        pmr_obj.update(
            {
                "hip": hip_rec,
                "doctor": doc_rec,
                "appointment": appointment_rec,
                "patient": patient_rec,
            }
        )
        logging.info(f"{pmr_obj=}")
        dummy_fhir = {
            "identifier": {
                "system": "http://hip.in",
                "value": "1ad6c4a6-b049-11ee-9c45-0050568837bb",
            },
            "entry": [
                {
                    "resource": {
                        "date": "2024-01-04T15:36:45+05:30",
                        "custodian": {
                            "reference": "Organization/66",
                            "display": "Demo Hospital, Gujarat",
                        },
                        "meta": {
                            "lastUpdated": "2024-01-04T15:36:45+05:30",
                            "versionId": "1",
                            "profile": [
                                "https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord"
                            ],
                        },
                        "subject": {
                            "reference": "Patient/1ad3e934-b049-11ee-9c38-0050568837bb",
                            "display": "Sonu  Kumar",
                        },
                        "author": [
                            {
                                "reference": "Practitioner/1ad3e902-b049-11ee-9c37-0050568837bb",
                                "display": "doctor  desk",
                            }
                        ],
                        "section": [
                            {
                                "entry": [
                                    {
                                        "reference": "MedicationRequest/1ad6aa0c-b049-11ee-9c41-0050568837bb"
                                    },
                                    {
                                        "reference": "MedicationRequest/1ad6ac14-b049-11ee-9c43-0050568837bb"
                                    },
                                ],
                                "code": {
                                    "coding": [
                                        {
                                            "system": "http://snomed.info/sct",
                                            "code": "721912009",
                                            "display": "Medication summary document",
                                        }
                                    ]
                                },
                                "title": "Medications",
                            },
                            {
                                "entry": [
                                    {
                                        "reference": "Condition/1ad5326c-b049-11ee-9c39-0050568837bb"
                                    }
                                ],
                                "code": {
                                    "coding": [
                                        {
                                            "system": "http://snomed.info/sct",
                                            "code": "422843007",
                                            "display": "Chief complaint section",
                                        }
                                    ]
                                },
                                "title": "Chief Complaints",
                            },
                            {
                                "entry": [
                                    {
                                        "reference": "Condition/1ad53410-b049-11ee-9c3a-0050568837bb"
                                    }
                                ],
                                "code": {
                                    "coding": [
                                        {
                                            "system": "http://snomed.info/sct",
                                            "code": "371529009",
                                            "display": "History and physical report",
                                        }
                                    ]
                                },
                                "title": "Medical History",
                            },
                            {
                                "entry": [
                                    {
                                        "reference": "Observation/height1ad3e8d0-b049-11ee-9c36-0050568837bb"
                                    },
                                    {
                                        "reference": "Observation/weight1ad3e8d0-b049-11ee-9c36-0050568837bb"
                                    },
                                    {
                                        "reference": "Observation/bmi1ad3e8d0-b049-11ee-9c36-0050568837bb"
                                    },
                                    {
                                        "reference": "Observation/temperature1ad3e8d0-b049-11ee-9c36-0050568837bb"
                                    },
                                    {
                                        "reference": "Observation/dbp1ad3e8d0-b049-11ee-9c36-0050568837bb"
                                    },
                                    {
                                        "reference": "Observation/sbp1ad3e8d0-b049-11ee-9c36-0050568837bb"
                                    },
                                    {
                                        "reference": "Observation/rr1ad3e8d0-b049-11ee-9c36-0050568837bb"
                                    },
                                    {
                                        "reference": "Observation/pulse1ad3e8d0-b049-11ee-9c36-0050568837bb"
                                    },
                                    {
                                        "reference": "Observation/1ad53a5a-b049-11ee-9c3f-0050568837bb"
                                    },
                                ],
                                "code": {
                                    "coding": [
                                        {
                                            "system": "http://snomed.info/sct",
                                            "code": "425044008",
                                            "display": "Physical exam section",
                                        }
                                    ]
                                },
                                "title": "Physical Examination",
                            },
                            {
                                "entry": [
                                    {
                                        "reference": "AllergyIntolerance/1ad5392e-b049-11ee-9c3e-0050568837bb"
                                    },
                                    {
                                        "reference": "AllergyIntolerance/1ad53802-b049-11ee-9c3d-0050568837bb"
                                    },
                                ],
                                "code": {
                                    "coding": [
                                        {
                                            "system": "http://snomed.info/sct",
                                            "code": "722446000",
                                            "display": "Allergy record",
                                        }
                                    ]
                                },
                                "title": "Allergy Section",
                            },
                            {
                                "entry": [
                                    {
                                        "reference": "ServiceRequest/1ad5355a-b049-11ee-9c3b-0050568837bb"
                                    },
                                    {
                                        "reference": "ServiceRequest/1ad53690-b049-11ee-9c3c-0050568837bb"
                                    },
                                    {
                                        "reference": "ServiceRequest/1ad53b9a-b049-11ee-9c40-0050568837bb"
                                    },
                                ],
                                "code": {
                                    "coding": [
                                        {
                                            "system": "http://snomed.info/sct",
                                            "code": "721963009",
                                            "display": "Order document",
                                        }
                                    ]
                                },
                                "title": "Investigation Advice",
                            },
                        ],
                        "id": "1ad3e826-b049-11ee-9c34-0050568837bb",
                        "encounter": {
                            "reference": "Encounter/1ad3e89e-b049-11ee-9c35-0050568837bb"
                        },
                        "type": {
                            "coding": [
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "371530004",
                                    "display": "Clinical consultation report",
                                }
                            ],
                            "text": "Clinical Consultation report",
                        },
                        "title": "Consultation Report",
                        "resourceType": "Composition",
                        "status": "final",
                    },
                    "fullUrl": "Composition/1ad3e826-b049-11ee-9c34-0050568837bb",
                },
                {
                    "resource": {
                        "identifier": [
                            {
                                "system": "https://doctor.ndhm.gov.in",
                                "type": {
                                    "coding": [
                                        {
                                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                            "code": "MD",
                                            "display": "Medical License number",
                                        }
                                    ]
                                },
                                "value": "21-1521-3828-3227",
                            }
                        ],
                        "meta": {
                            "lastUpdated": "2024-01-04T15:36:45+05:30",
                            "versionId": "1",
                            "profile": [
                                "https://nrces.in/ndhm/fhir/r4/StructureDefinition/Practitioner"
                            ],
                        },
                        "name": [{"text": "doctor  desk"}],
                        "id": "1ad3e902-b049-11ee-9c37-0050568837bb",
                        "resourceType": "Practitioner",
                    },
                    "fullUrl": "Practitioner/1ad3e902-b049-11ee-9c37-0050568837bb",
                },
                {
                    "resource": {
                        "identifier": [
                            {
                                "system": "https://facility.ndhm.gov.in",
                                "type": {
                                    "coding": [
                                        {
                                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                            "code": "PRN",
                                            "display": "Provider number",
                                        }
                                    ]
                                },
                                "value": "4567823",
                            }
                        ],
                        "meta": {
                            "profile": [
                                "https://nrces.in/ndhm/fhir/r4/StructureDefinition/Organization"
                            ]
                        },
                        "name": "Demo Hospital, Gujarat",
                        "telecom": [
                            {
                                "system": "phone",
                                "use": "work",
                                "value": "+91 0120-6933404",
                            },
                            {
                                "system": "email",
                                "use": "work",
                                "value": "support-ngehospital@nic.in",
                            },
                        ],
                        "id": "66",
                        "resourceType": "Organization",
                    },
                    "fullUrl": "Organization/66",
                },
                {
                    "resource": {
                        "identifier": [
                            {
                                "system": "https://healthid.ndhm.gov.in",
                                "type": {
                                    "coding": [
                                        {
                                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                            "code": "MR",
                                            "display": "Medical record number",
                                        }
                                    ]
                                },
                                "value": "22-7225-4829-5255",
                            }
                        ],
                        "gender": "male",
                        "meta": {
                            "lastUpdated": "2024-01-04T15:36:45+05:30",
                            "versionId": "1",
                            "profile": [
                                "https://nrces.in/ndhm/fhir/r4/StructureDefinition/Patient"
                            ],
                        },
                        "name": [{"text": "Sonu  Kumar"}],
                        "telecom": [
                            {"system": "phone", "use": "home", "value": "+918882458079"}
                        ],
                        "id": "1ad3e934-b049-11ee-9c38-0050568837bb",
                        "birthDate": "1991",
                        "resourceType": "Patient",
                    },
                    "fullUrl": "Patient/1ad3e934-b049-11ee-9c38-0050568837bb",
                },
                {
                    "resource": {
                        "code": {
                            "text": "Faroeze 200 mg oral tablet(Faropenem (as faropenem sodium) 200 mg oral tablet)"
                        },
                        "id": "1ad6aa7a-b049-11ee-9c42-0050568837bb",
                        "resourceType": "Medication",
                    },
                    "fullUrl": "Medication/1ad6aa7a-b049-11ee-9c42-0050568837bb",
                },
                {
                    "resource": {
                        "code": {
                            "text": "Utamide 50 mg oral tablet(Bicalutamide 50 mg oral tablet)"
                        },
                        "id": "1ad6ac3c-b049-11ee-9c44-0050568837bb",
                        "resourceType": "Medication",
                    },
                    "fullUrl": "Medication/1ad6ac3c-b049-11ee-9c44-0050568837bb",
                },
                {
                    "resource": {
                        "requester": {
                            "reference": "Practitioner/1ad3e902-b049-11ee-9c37-0050568837bb"
                        },
                        "medicationReference": {
                            "reference": "Medication/1ad6aa7a-b049-11ee-9c42-0050568837bb"
                        },
                        "authoredOn": "2024-01-04T15:36:45+05:30",
                        "dosageInstruction": [{"text": "(1)-Twice a day (Duration:7)"}],
                        "subject": {
                            "reference": "Patient/1ad3e934-b049-11ee-9c38-0050568837bb"
                        },
                        "id": "1ad6aa0c-b049-11ee-9c41-0050568837bb",
                        "intent": "order",
                        "resourceType": "MedicationRequest",
                        "status": "active",
                    },
                    "fullUrl": "MedicationRequest/1ad6aa0c-b049-11ee-9c41-0050568837bb",
                },
                {
                    "resource": {
                        "requester": {
                            "reference": "Practitioner/1ad3e902-b049-11ee-9c37-0050568837bb"
                        },
                        "medicationReference": {
                            "reference": "Medication/1ad6ac3c-b049-11ee-9c44-0050568837bb"
                        },
                        "authoredOn": "2024-01-04T15:36:45+05:30",
                        "dosageInstruction": [{"text": "(1)-Twice a day (Duration:8)"}],
                        "subject": {
                            "reference": "Patient/1ad3e934-b049-11ee-9c38-0050568837bb"
                        },
                        "id": "1ad6ac14-b049-11ee-9c43-0050568837bb",
                        "intent": "order",
                        "resourceType": "MedicationRequest",
                        "status": "active",
                    },
                    "fullUrl": "MedicationRequest/1ad6ac14-b049-11ee-9c43-0050568837bb",
                },
                {
                    "resource": {
                        "code": {"text": "Height"},
                        "effectiveDateTime": "2024-01-04T15:35:17+05:30",
                        "id": "height1ad3e8d0-b049-11ee-9c36-0050568837bb",
                        "resourceType": "Observation",
                        "status": "final",
                        "valueQuantity": {"unit": "CM", "value": 170},
                    },
                    "fullUrl": "Observation/height1ad3e8d0-b049-11ee-9c36-0050568837bb",
                },
                {
                    "resource": {
                        "code": {"text": "Weight"},
                        "effectiveDateTime": "2024-01-04T15:35:17+05:30",
                        "id": "weight1ad3e8d0-b049-11ee-9c36-0050568837bb",
                        "resourceType": "Observation",
                        "status": "final",
                        "valueQuantity": {"unit": "Kg", "value": 68},
                    },
                    "fullUrl": "Observation/weight1ad3e8d0-b049-11ee-9c36-0050568837bb",
                },
                {
                    "resource": {
                        "code": {"text": "BMI"},
                        "effectiveDateTime": "2024-01-04T15:35:17+05:30",
                        "id": "bmi1ad3e8d0-b049-11ee-9c36-0050568837bb",
                        "resourceType": "Observation",
                        "status": "final",
                        "valueQuantity": {"unit": "kg/m2", "value": 23.53},
                    },
                    "fullUrl": "Observation/bmi1ad3e8d0-b049-11ee-9c36-0050568837bb",
                },
                {
                    "resource": {
                        "code": {"text": "Temperature"},
                        "effectiveDateTime": "2024-01-04T15:35:17+05:30",
                        "id": "temperature1ad3e8d0-b049-11ee-9c36-0050568837bb",
                        "resourceType": "Observation",
                        "status": "final",
                        "valueQuantity": {"unit": "°F", "value": 99},
                    },
                    "fullUrl": "Observation/temperature1ad3e8d0-b049-11ee-9c36-0050568837bb",
                },
                {
                    "resource": {
                        "code": {"text": "Systolic Blood pressure"},
                        "effectiveDateTime": "2024-01-04T15:35:17+05:30",
                        "id": "sbp1ad3e8d0-b049-11ee-9c36-0050568837bb",
                        "resourceType": "Observation",
                        "status": "final",
                        "valueQuantity": {"unit": "mmHg", "value": 126},
                    },
                    "fullUrl": "Observation/sbp1ad3e8d0-b049-11ee-9c36-0050568837bb",
                },
                {
                    "resource": {
                        "code": {"text": "Diastolic Blood pressure"},
                        "effectiveDateTime": "2024-01-04T15:35:17+05:30",
                        "id": "dbp1ad3e8d0-b049-11ee-9c36-0050568837bb",
                        "resourceType": "Observation",
                        "status": "final",
                        "valueQuantity": {"unit": "mmHg", "value": 82},
                    },
                    "fullUrl": "Observation/dbp1ad3e8d0-b049-11ee-9c36-0050568837bb",
                },
                {
                    "resource": {
                        "code": {"text": "Respiratory Rate"},
                        "effectiveDateTime": "2024-01-04T15:35:17+05:30",
                        "id": "rr1ad3e8d0-b049-11ee-9c36-0050568837bb",
                        "resourceType": "Observation",
                        "status": "final",
                        "valueQuantity": {"unit": "RPM", "value": 46},
                    },
                    "fullUrl": "Observation/rr1ad3e8d0-b049-11ee-9c36-0050568837bb",
                },
                {
                    "resource": {
                        "code": {"text": "Pulse"},
                        "effectiveDateTime": "2024-01-04T15:35:17+05:30",
                        "id": "pulse1ad3e8d0-b049-11ee-9c36-0050568837bb",
                        "resourceType": "Observation",
                        "status": "final",
                        "valueQuantity": {"unit": "BPM", "value": 75},
                    },
                    "fullUrl": "Observation/pulse1ad3e8d0-b049-11ee-9c36-0050568837bb",
                },
                {
                    "resource": {
                        "code": {"text": "DIAGNOSIS"},
                        "valueString": "Lassa fever",
                        "effectiveDateTime": "2024-01-04T15:36:11+05:30",
                        "id": "1ad53a5a-b049-11ee-9c3f-0050568837bb",
                        "resourceType": "Observation",
                        "status": "final",
                    },
                    "fullUrl": "Observation/1ad53a5a-b049-11ee-9c3f-0050568837bb",
                },
                {
                    "resource": {
                        "code": {"text": "Human rabies"},
                        "onsetPeriod": {"start": "2024-01-04T15:35:28+05:30"},
                        "subject": {
                            "reference": "Patient/1ad3e934-b049-11ee-9c38-0050568837bb"
                        },
                        "recordedDate": "2024-01-04T15:35:28+05:30",
                        "id": "1ad5326c-b049-11ee-9c39-0050568837bb",
                        "clinicalStatus": {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                                    "code": "active",
                                    "display": "active",
                                }
                            ],
                            "text": "COMPLAIN",
                        },
                        "category": [
                            {
                                "coding": [
                                    {
                                        "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                                        "code": "problem-list-item",
                                        "display": "Problem List Item",
                                    }
                                ],
                                "text": "problem list",
                            }
                        ],
                        "resourceType": "Condition",
                    },
                    "fullUrl": "Condition/1ad5326c-b049-11ee-9c39-0050568837bb",
                },
                {
                    "resource": {
                        "code": {"text": "Barbers' rash"},
                        "onsetPeriod": {"start": "2024-01-04T15:35:36+05:30"},
                        "subject": {
                            "reference": "Patient/1ad3e934-b049-11ee-9c38-0050568837bb"
                        },
                        "recordedDate": "2024-01-04T15:35:36+05:30",
                        "id": "1ad53410-b049-11ee-9c3a-0050568837bb",
                        "clinicalStatus": {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                                    "code": "active",
                                    "display": "active",
                                }
                            ],
                            "text": "HISTORY",
                        },
                        "category": [
                            {
                                "coding": [
                                    {
                                        "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                                        "code": "problem-list-item",
                                        "display": "Problem List Item",
                                    }
                                ],
                                "text": "problem list",
                            }
                        ],
                        "resourceType": "Condition",
                    },
                    "fullUrl": "Condition/1ad53410-b049-11ee-9c3a-0050568837bb",
                },
                {
                    "resource": {
                        "requester": {
                            "reference": "Practitioner/1ad3e902-b049-11ee-9c37-0050568837bb"
                        },
                        "code": {"text": "ZN staining for AFB"},
                        "authoredOn": "2024-01-04T15:35:43+05:30",
                        "subject": {
                            "reference": "Patient/1ad3e934-b049-11ee-9c38-0050568837bb"
                        },
                        "id": "1ad5355a-b049-11ee-9c3b-0050568837bb",
                        "category": [
                            {
                                "coding": [
                                    {
                                        "system": "http://snomed.info/sct",
                                        "code": "108252007",
                                        "display": "Laboratory procedure",
                                    }
                                ]
                            }
                        ],
                        "intent": "order",
                        "resourceType": "ServiceRequest",
                        "status": "active",
                    },
                    "fullUrl": "ServiceRequest/1ad5355a-b049-11ee-9c3b-0050568837bb",
                },
                {
                    "resource": {
                        "requester": {
                            "reference": "Practitioner/1ad3e902-b049-11ee-9c37-0050568837bb"
                        },
                        "code": {"text": "A.P. & OBLIQUE VIEW OF HAND"},
                        "authoredOn": "2024-01-04T15:35:48+05:30",
                        "subject": {
                            "reference": "Patient/1ad3e934-b049-11ee-9c38-0050568837bb"
                        },
                        "id": "1ad53690-b049-11ee-9c3c-0050568837bb",
                        "category": [
                            {
                                "coding": [
                                    {
                                        "system": "http://snomed.info/sct",
                                        "code": "168501001",
                                        "display": "Radiology result abnormal",
                                    }
                                ]
                            }
                        ],
                        "intent": "order",
                        "resourceType": "ServiceRequest",
                        "status": "active",
                    },
                    "fullUrl": "ServiceRequest/1ad53690-b049-11ee-9c3c-0050568837bb",
                },
                {
                    "resource": {
                        "requester": {
                            "reference": "Practitioner/1ad3e902-b049-11ee-9c37-0050568837bb"
                        },
                        "code": {"text": "USG B-SCAN"},
                        "authoredOn": "2024-01-04T18:21:24+05:30",
                        "subject": {
                            "reference": "Patient/1ad3e934-b049-11ee-9c38-0050568837bb"
                        },
                        "id": "1ad53b9a-b049-11ee-9c40-0050568837bb",
                        "category": [
                            {
                                "coding": [
                                    {
                                        "system": "http://snomed.info/sct",
                                        "code": "721964003",
                                        "display": "Radiology order",
                                    }
                                ]
                            }
                        ],
                        "intent": "order",
                        "resourceType": "ServiceRequest",
                        "status": "active",
                    },
                    "fullUrl": "ServiceRequest/1ad53b9a-b049-11ee-9c40-0050568837bb",
                },
                {
                    "resource": {
                        "code": {
                            "coding": [
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "387264003",
                                    "display": "Diazepam",
                                }
                            ]
                        },
                        "asserter": {
                            "reference": "Practitioner/1ad3e902-b049-11ee-9c37-0050568837bb"
                        },
                        "verificationStatus": {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                                    "code": "confirmed",
                                    "display": "Confirmed",
                                }
                            ]
                        },
                        "patient": {
                            "reference": "Patient/1ad3e934-b049-11ee-9c38-0050568837bb"
                        },
                        "id": "1ad5392e-b049-11ee-9c3e-0050568837bb",
                        "clinicalStatus": {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                                    "code": "active",
                                    "display": "Active",
                                }
                            ]
                        },
                        "type": "allergy",
                        "category": ["food"],
                        "resourceType": "AllergyIntolerance",
                    },
                    "fullUrl": "AllergyIntolerance/1ad5392e-b049-11ee-9c3e-0050568837bb",
                },
                {
                    "resource": {
                        "code": {
                            "coding": [
                                {
                                    "system": "http://snomed.info/sct",
                                    "code": "387096002",
                                    "display": "Dapsone",
                                }
                            ]
                        },
                        "asserter": {
                            "reference": "Practitioner/1ad3e902-b049-11ee-9c37-0050568837bb"
                        },
                        "verificationStatus": {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
                                    "code": "confirmed",
                                    "display": "Confirmed",
                                }
                            ]
                        },
                        "patient": {
                            "reference": "Patient/1ad3e934-b049-11ee-9c38-0050568837bb"
                        },
                        "id": "1ad53802-b049-11ee-9c3d-0050568837bb",
                        "clinicalStatus": {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                                    "code": "active",
                                    "display": "Active",
                                }
                            ]
                        },
                        "type": "allergy",
                        "category": ["food"],
                        "resourceType": "AllergyIntolerance",
                    },
                    "fullUrl": "AllergyIntolerance/1ad53802-b049-11ee-9c3d-0050568837bb",
                },
                {
                    "resource": {
                        "identifier": [{"system": "https://ndhm.in", "value": "S100"}],
                        "meta": {
                            "lastUpdated": "2024-01-04T15:36:45+05:30",
                            "profile": [
                                "https://nrces.in/ndhm/fhir/r4/StructureDefinition/Encounter"
                            ],
                        },
                        "subject": {
                            "reference": "Patient/1ad3e934-b049-11ee-9c38-0050568837bb"
                        },
                        "id": "1ad3e89e-b049-11ee-9c35-0050568837bb",
                        "class": {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                            "code": "AMB",
                            "display": "ambulatory",
                        },
                        "resourceType": "Encounter",
                        "status": "finished",
                    },
                    "fullUrl": "Encounter/1ad3e89e-b049-11ee-9c35-0050568837bb",
                },
            ],
            "meta": {
                "lastUpdated": "2024-01-11T11:47:32+05:30",
                "versionId": "1",
                "security": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-Confidentiality",
                        "code": "V",
                        "display": "very restricted",
                    }
                ],
                "profile": [
                    "https://nrces.in/ndhm/fhir/r4/StructureDefinition/DocumentBundle"
                ],
            },
            "id": "1ad6c4a6-b049-11ee-9c45-0050568837bb",
            "type": "document",
            "resourceType": "Bundle",
            "timestamp": "2024-01-04T15:36:45+05:30",
        }
        return dummy_fhir


def opConsultStructured(bundle_name: str, bundle_identifier: str, pmr_id: str):
    try:
        logging.info("executing opConsultStructured function")
        time_str = datetime.now(timezone).isoformat()
        logging.info(f"Getting PMR Object")
        pmr_obj = CRUDPatientMedicalRecord().read(pmr_id=pmr_id)
        if pmr_obj:
            logging.info(f"Getting Doctor record")
            doc_rec = CRUDDocDetails().read_by_docId(doc_id=pmr_obj["doc_id"])
            logging.info(f"Getting Appointment record")
            appointment_rec = CRUDAppointments().read(
                appointment_id=pmr_obj["appointment_id"]
            )
            logging.info(f"Getting HIP record")
            hip_rec = CRUDHIP().read(hip_ip=pmr_obj["hip_id"])
            logging.info(f"Getting Patient record")
            patient_rec = CRUDPatientDetails().read_by_patientId(
                patient_id=pmr_obj["patient_id"]
            )
            pmr_obj.update(
                {
                    "hip": hip_rec,
                    "doctor": doc_rec,
                    "appointment": appointment_rec,
                    "patient": patient_rec,
                }
            )
            ref_data, bundle_entry_list = [], []
            logging.info(f"{pmr_obj=}")
            doctor_obj = pmr_obj.get("doctor")
            logging.info(f"{doctor_obj=}")
            # Create Practitioner Record
            logging.info("Create Practitioner Record")
            practitioner_ref_id = str(uuid.uuid4())
            practitioner_bundle = get_practitioner_construct(
                practitioner_info={
                    "practitioner_ref_id": practitioner_ref_id,
                    "name": doctor_obj["doc_name"],
                    "gender": "Female",
                    "practitioner_id": doctor_obj["doc_licence_no"],
                    "telecom": "1234567890",
                }
            )
            practitioner_ref = Reference.construct(
                reference=f"Practitioner/{practitioner_bundle.id}",
                display=doctor_obj["doc_name"],
            )
            bundle_entry_list.append(
                BundleEntry.construct(
                    fullUrl=f"Practitioner/{practitioner_bundle.id}",
                    resource=practitioner_bundle,
                )
            )
            ref_data.append(practitioner_ref)

            # Creating Organization Entry
            hip_obj = pmr_obj.get("hip")
            logging.info(f"{hip_obj=}")
            logging.info("Creating Organization Entry")
            organization_ref_id = str(uuid.uuid4())
            organization_bundle = get_organization_construct(
                organization_info={
                    "name": hip_obj["name"],
                    "organization_id": organization_ref_id,
                }
            )
            bundle_entry_list.append(
                BundleEntry.construct(
                    fullUrl=f"Organization/{organization_bundle.id}",
                    resource=organization_bundle,
                )
            )
            organization_ref = Reference.construct(
                reference=f"Organization/{organization_bundle.id}",
                display=hip_obj["name"],
            )
            ref_data.append(organization_ref)

            # Creating Patient Entry
            logging.info("Creating Patient Entry")
            patient_obj = pmr_obj.get("patient")
            logging.info(f"{patient_obj=}")
            logging.info(f"Creating Patient Entry")
            patient_ref_id = str(uuid.uuid4())
            patient_bundle = get_patient_construct(
                patient_info={
                    "name": patient_obj["name"],
                    "gender": "male" if patient_obj["gender"] == "M" else "female",
                    "patient_id": patient_ref_id,
                    "telecom": patient_obj["mobile_number"],
                }
            )
            bundle_entry_list.append(
                BundleEntry.construct(
                    fullUrl=f"Patient/{patient_bundle.id}",
                    resource=patient_bundle,
                )
            )
            patient_ref = Reference.construct(
                reference=f"Patient/{patient_bundle.id}",
                display=patient_bundle.name[0]["text"],
            )
            ref_data.append(patient_bundle)

            # Creating Encounter Entry
            logging.info(f"Creating Encounter Entry")
            appointment_obj = pmr_obj.get("appointment")
            logging.info(f"{appointment_obj=}")
            slot_id = appointment_obj.get("slot_id")
            slot_obj = CRUDSlots().read(slot_id=slot_id)
            logging.info(f"{slot_obj=}")
            encounter_start = datetime.combine(slot_obj["date"], slot_obj["start_time"])
            encounter_end = datetime.combine(slot_obj["date"], slot_obj["end_time"])
            encounter_ref_id = str(uuid.uuid4())
            encounter_bundle = Encounter.construct(
                id=encounter_ref_id,
                status="finished",
                subject=patient_ref,
                class_fhir=Coding.construct(
                    system="http://terminology.hl7.org/CodeSystem/v3-ActCode",
                    code=appointment_obj["encounter_type_code"],
                    display=appointment_obj["encounter_type"],
                ),
            )
            bundle_entry_list.append(
                BundleEntry.construct(
                    fullUrl=f"Encounter/{encounter_bundle.id}",
                    resource=encounter_bundle,
                )
            )
            encounter_ref = Reference.construct(
                reference=f"Encounter/{encounter_bundle.id}",
                display="Encounter/OP Consult Record",
            )
            ref_data.append(encounter_ref)

            # Creating ChiefComplaint/Conditions
            logging.info(f"Creating ChiefComplaint/Conditions Entry")
            sympt_list = CRUDSymptoms().read_by_pmrId(pmr_id=pmr_id)
            logging.info(f"{sympt_list=}")
            condition_sections = [
                get_condition_construct(
                    condition_id=str(uuid.uuid4()),
                    clinical_code=sympt_obj["snowmed_code"],
                    clinical_display=sympt_obj["snowmed_display"],
                    patient_ref=patient_obj["id"],
                    encounter_ref=appointment_obj["id"],
                )
                for sympt_obj in sympt_list
            ]
            bundle_entry_list.extend(
                [
                    BundleEntry.construct(
                        fullUrl=f"Condition/{condition_bundle.id}",
                        resource=condition_bundle,
                    )
                    for condition_bundle in condition_sections
                ]
            )
            ref_data.extend(condition_sections)
            codeable_obj = CodeableConcept()
            codeable_obj.coding = [
                {
                    "system": "http://snomed.info/sct",
                    "code": "422843007",
                    "display": "Chief complaint section",
                }
            ]
            condition_entry = [
                Reference.construct(reference=f"Condition/{section.id}")
                for section in condition_sections
            ]
            section_refs = [
                {
                    "title": "Chief complaints",
                    "entry": condition_entry,
                    "code": codeable_obj,
                }
            ]

            # Creating physical examination
            physical_examination_bundle_list = []
            logging.info(f"Creating Vitals Entry")
            vital_obj = CRUDVital().read_by_pmrId(pmr_id=pmr_id)
            physical_examination = f"Temperature {vital_obj['body_temperature']} Blood Pressure {vital_obj['systolic_blood_pressure']}/{vital_obj['diastolic_blood_pressure']}"
            physical_examination_temp_bundle = get_observation_construct(
                observation_id=str(uuid.uuid4()),
                clinical_display=physical_examination,
                patient_ref=patient_obj["id"],
                encounter_ref=appointment_obj["id"],
                observation_type="Temperature",
                observation_unit="F",
                observation_value=vital_obj["body_temperature"],
            )
            physical_examination_bundle_list.append(physical_examination_temp_bundle)
            ref_data.append(physical_examination_temp_bundle)
            bundle_entry_list.append(
                BundleEntry.construct(
                    fullUrl=f"PhysicalExamination/{physical_examination_temp_bundle.id}",
                    resource=physical_examination_temp_bundle,
                )
            )
            physical_examination_sbp_bundle = get_observation_construct(
                observation_id=str(uuid.uuid4()),
                clinical_display=physical_examination,
                patient_ref=patient_obj["id"],
                encounter_ref=appointment_obj["id"],
                observation_type="Systolic Blood pressure",
                observation_unit="mmHg",
                observation_value=vital_obj["systolic_blood_pressure"],
            )
            # physical_examination = create_section(
            #     ref_id=vital_obj["id"],
            #     title="Physical Examination",
            #     code="422843007",
            #     display="Physical Examination section",
            #     text=physical_examination,
            # )
            ref_data.append(physical_examination_sbp_bundle)
            physical_examination_bundle_list.append(physical_examination_sbp_bundle)
            bundle_entry_list.append(
                BundleEntry.construct(
                    fullUrl=f"PhysicalExamination/{physical_examination_sbp_bundle.id}",
                    resource=physical_examination_sbp_bundle,
                )
            )

            physical_examination_dbp_bundle = get_observation_construct(
                observation_id=str(uuid.uuid4()),
                clinical_display=physical_examination,
                patient_ref=patient_obj["id"],
                encounter_ref=appointment_obj["id"],
                observation_type="Diastolic Blood pressure",
                observation_unit="mmHg",
                observation_value=vital_obj["diastolic_blood_pressure"],
            )
            # physical_examination = create_section(
            #     ref_id=vital_obj["id"],
            #     title="Physical Examination",
            #     code="422843007",
            #     display="Physical Examination section",
            #     text=physical_examination,
            # )
            physical_examination_bundle_list.append(physical_examination_dbp_bundle)
            ref_data.append(physical_examination_dbp_bundle)
            bundle_entry_list.append(
                BundleEntry.construct(
                    fullUrl=f"PhysicalExamination/{physical_examination_dbp_bundle.id}",
                    resource=physical_examination_dbp_bundle,
                )
            )
            codeable_obj = CodeableConcept()
            codeable_obj.coding = [
                {
                    "system": "http://snomed.info/sct",
                    "code": "425044008",
                    "display": "Physical exam section",
                }
            ]
            physical_examination_entry = [
                Reference.construct(
                    reference=f"PhysicalExamination/{physical_examination_bundle.id}"
                )
                for physical_examination_bundle in physical_examination_bundle_list
            ]
            phy_exam_ref = {
                "title": "Physical Examination",
                "entry": physical_examination_entry,
                "code": codeable_obj,
            }
            section_refs.append(phy_exam_ref)

            # # Creating medical history
            # logging.info(f"Creating medical history")
            # medical_history_list = CRUDMedicalHistory().read_self_by_pmrId(
            #     pmr_id=pmr_id
            # )
            # med_history_sections = [
            #     create_section(
            #         title="Medical History",
            #         code="371529009",
            #         ref_id=medical_history_obj["id"],
            #         display="Medical History section",
            #         text=medical_history_obj["medical_history"],
            #     )
            #     for medical_history_obj in medical_history_list
            # ]
            # ref_data.extend(med_history_sections)
            # med_history_ref = [
            #     Reference.construct(
            #         reference=f"MedicalHistory/{med_history_section.id}",
            #         display=f"{med_history_section.title}",
            #     )
            #     for med_history_section in med_history_sections
            # ]
            # section_refs.extend(med_history_ref)

            # # Creating family medical history
            # logging.info(f"Creating family medical history")
            # family_medical_history_list = CRUDMedicalHistory().read_others_by_pmrId(
            #     pmr_id=pmr_id
            # )
            # family_med_history_sections = [
            #     create_section(
            #         title="Family History",
            #         code="371529009",
            #         ref_id=family_medical_history_obj["id"],
            #         display="Family History section",
            #         text=family_medical_history_obj["medical_history"],
            #     )
            #     for family_medical_history_obj in family_medical_history_list
            # ]
            # ref_data.extend(family_med_history_sections)
            # family_med_history_ref = [
            #     Reference.construct(
            #         reference=f"FamilyHistory/{family_med_history_section.id}",
            #         display=f"{family_med_history_section.title}",
            #     )
            #     for family_med_history_section in family_med_history_sections
            # ]
            # section_refs.extend(family_med_history_ref)

            # Creating medication history
            logging.info(f"Creating medication history")
            medicines_list = CRUDMedicines().read_by_pmrId(pmr_id=pmr_id)
            logging.info(f"{medicines_list=}")
            # medicines_sections = [
            #     get_medical_statement_construct(
            #         patient_ref=patient_ref_id,
            #         medication_obj_code=medicines_obj["snowmed_code"],
            #         medication_obj_display=medicines_obj["snowmed_display"],
            #         medication_statement_id=str(uuid.uuid4()),
            #     )
            #     for medicines_obj in medicines_list
            # ]
            medicines_req_sections, medicines_sections = [], []
            for medicines_obj in medicines_list:
                medication_request_id = str(uuid.uuid4())
                medication_request_bundle, medicine_bundle = (
                    get_medication_request_construct(
                        medication_request_id=medication_request_id,
                        dosage=f"{medicines_obj['dosage']}|{medicines_obj['frequency']}|{medicines_obj['time_of_day']}|{medicines_obj['duration_period']}",
                        patient_ref=patient_ref_id,
                        practitioner_ref=practitioner_ref_id,
                        medicine_name=medicines_obj["medicine_name"],
                    )
                )
                medicines_req_sections.append(medication_request_bundle)
                medicines_sections.append(medicine_bundle)
            logging.info(f"{medicines_req_sections=}")
            codeable_obj = CodeableConcept()
            codeable_obj.coding = [
                {
                    "system": "http://snomed.info/sct",
                    "code": "721912009",
                    "display": "Medication summary document",
                }
            ]
            medicines_entry = [
                Reference.construct(
                    reference=f"MedicationRequest/{medicines_req_bundle['id']}"
                )
                for medicines_req_bundle in medicines_req_sections
            ]
            medicines_ref = {
                "title": "Medications",
                "entry": medicines_entry,
                "code": codeable_obj,
            }
            section_refs.append(medicines_ref)
            bundle_entry_list.extend(
                [
                    BundleEntry.construct(
                        fullUrl=f"Medication/{medicines_bundle.id}",
                        resource=medicines_bundle,
                    )
                    for medicines_bundle in medicines_sections
                ]
            )
            bundle_entry_list.extend(
                [
                    BundleEntry.construct(
                        fullUrl=f"MedicationRequest/{medicines_req_bundle['id']}",
                        resource=medicines_req_bundle,
                    )
                    for medicines_req_bundle in medicines_req_sections
                ]
            )

            # Create Composition resource for OP Consult Record
            logging.info(f"Creating composition")
            composition = Composition.construct(
                id=str(uuid.uuid4()),
                title="OP Consult Record",
                date=slot_obj["date"],
                status="final",  # final | amended | entered-in-error | preliminary,
                type=CodeableConcept.construct(
                    text="OP Consult Record",
                    coding=[
                        {
                            "system": "http://snomed.info/sct",
                            "code": "371530004",
                            "display": "Clinical consultation report",
                        }
                    ],
                ),
                custodian=organization_ref,
                encounter=encounter_ref,
                author=[practitioner_ref],
                subject=patient_ref,
                section=section_refs,
            )
            # Coding.construct(
            #     system="http://snomed.info/sct",
            #     code="371530004",
            #     display="Clinical consultation report",
            # ),
            identifier = Identifier()
            identifier.value = bundle_identifier
            meta = Meta(
                versionId=1,
                lastUpdated=time_str,
                profile=[
                    "https://nrces.in/ndhm/fhir/r4/StructureDefinition/DocumentBundle"
                ],
                security=[
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-Confidentiality",
                        "code": "V",
                        "display": "very restricted",
                    }
                ],
            )
            identifier = Identifier()
            identifier.value = bundle_identifier
            identifier.system = "http://hip.in"
            logging.info(f"Creating bundle")
            bundle = Bundle.construct()
            bundle.type = "document"
            bundle.id = bundle_name
            bundle.meta = meta
            bundle.timestamp = time_str
            bundle.identifier = identifier
            bundle.entry = [
                BundleEntry.construct(
                    fullUrl=f"Composition/{composition.id}", resource=composition
                )
            ]
            bundle.entry.extend(bundle_entry_list)
            bundle_dict = bundle.__dict__
            bundle_json = JSONResponse(content=jsonable_encoder(bundle_dict))
            content_bytes = bundle_json.body
            content_str = content_bytes.decode("utf-8")
            response_dict = json.loads(content_str)
            print(f"{response_dict=}")
            response_dict = remove_none_values(response_dict)
            response_dict["resourceType"] = response_dict.pop("resource_type")
            return response_dict

        logging.info(f"No record found for {pmr_id=}")
        return None
    except Exception as error:
        logging.error(f"Error in opConsultStructured : {error}")
