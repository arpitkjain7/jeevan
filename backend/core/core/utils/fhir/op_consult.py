# from core import logger
from datetime import datetime, timezone
from fhir.resources.bundle import Bundle, BundleEntry
from fhir.resources.meta import Meta
from fhir.resources.identifier import Identifier
import pytz
from core.utils.fhir.modules import *
from core.crud.hims_patientMedicalRecord_crud import CRUDPatientMedicalRecord
from core.crud.hims_slots_crud import CRUDSlots
from core.crud.hims_patientMedicalDocuments_crud import CRUDPatientMedicalDocuments
from core.utils.aws.s3_helper import get_object

# logging = logger(__name__)
timezone = pytz.timezone("Asia/Kolkata")


def opConsultDocument(bundle_name: str, bundle_identifier: str, pmr_id: str):
    time_str = datetime.now(timezone).isoformat()
    identifier = Identifier()
    identifier.value = bundle_identifier
    meta = Meta(
        versionId=1,
        lastUpdated=time_str,
        profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/DocumentBundle"],
        security=[
            {
                "system": "http://terminology.hl7.org/CodeSystem/v3-Confidentiality",
                "code": "V",
                "display": "very restricted",
            }
        ],
    )
    # Creating Practitioner Entry
    # pmr_obj = CRUDPatientMedicalRecord().read(pmr_id=pmr_id)
    pmr_obj = CRUDPatientMedicalRecord().read_details(pmr_id=pmr_id)[0]
    doctor_obj = pmr_obj.get("doctor")
    # doctor_id = pmr_obj.get("doc_id")
    # doc_obj = CRUDDocDetails().read_by_docId(doc_id=doctor_id)
    practitioner_bundle = BundleEntry()
    practitioner_bundle.fullUrl = f"Practitioner/{doctor_obj['id']}"
    practitioner_bundle.resource = practitioner(
        practitioner_id=doctor_obj["id"],
        medical_licence_number=doctor_obj["doc_licence_no"],
        practitioner_name=doctor_obj["doc_name"],
    )
    # Creating Organization Entry
    # hip_id = pmr_obj.get("hip_id")
    # hip_obj = CRUDHIP().read(hip_ip=hip_id)
    hip_obj = pmr_obj.get("hip")
    organization_bundle = BundleEntry()
    organization_bundle.fullUrl = f"Organization/{hip_obj['id']}"
    organization_bundle.resource = organization(
        organization_id=hip_obj["id"],
        organization_name=hip_obj["name"],
        organization_prn=hip_obj["hfr_reg_number"],
        organization_email_id=hip_obj["hip_email_address"],
        organization_phone_number=hip_obj["hip_contact_number"],
    )
    # Creating Patient Entry
    # patient_id = pmr_obj.get("patient_id")
    # patient_obj = CRUDPatientDetails().read_by_patientId(patient_id=patient_id)
    patient_obj = pmr_obj.get("patient")
    patient_bundle = BundleEntry()
    patient_bundle.fullUrl = f"Patient/{patient_obj['id']}"
    patient_bundle.resource = patient(
        patient_id=patient_obj["id"],
        patient_mobile_number=patient_obj["mobile_number"],
        patient_dob=patient_obj["DOB"],
        patient_gender=patient_obj["gender"],
        patient_abha_id=patient_obj["abha_number"],
        patient_name=patient_obj["name"],
    )
    # Creating Encounter Entry
    appointment_obj = pmr_obj.get("appointment")
    slot_id = appointment_obj.get("slot_id")
    slot_obj = CRUDSlots().read(slot_id=slot_id)
    encounter_bundle = BundleEntry()
    encounter_bundle.fullUrl = f"Encounter/{appointment_obj['id']}"
    encounter_bundle.resource = encounter(
        encounter_id=appointment_obj["id"],
        encounter_type_code=appointment_obj["encounter_type_code"],
        encounter_type_display=appointment_obj["encounter_type_code"],
        encounter_start=f"{slot_obj['date']} {slot_obj['start_time']}",
        encounter_end=f"{slot_obj['date']} {slot_obj['end_time']}",
        patient_reference=f"Patient/{patient_obj['id']}",
    )
    # Creating Appointment Entry
    appointment_obj = pmr_obj.get("appointment")
    appointment_bundle = BundleEntry()
    appointment_bundle.fullUrl = f"Appointment/{appointment_obj['id']}"
    appointment_bundle.resource = appointment(
        patient_ref=f"Patient/{patient_obj['id']}",
        practitioner_ref=f"Practitioner/{doctor_obj['id']}",
        status=appointment_obj["consultation_status"],
        start_timestamp=f"{slot_obj['date']} {slot_obj['start_time']}",
        end_timestamp=f"{slot_obj['date']} {slot_obj['end_time']}",
    )
    # Creating Document Entry
    pmr_document_list = CRUDPatientMedicalDocuments().read_by_pmr_id(pmr_id=pmr_id)
    document_bundle = BundleEntry()
    for pmr_document_obj in pmr_document_list:
        document_location = pmr_document_obj.get("document_location")
        bucket_name = document_location.split("/")[0]
        document_key = "/".join(document_location.split("/")[1:])
        document_content = get_object(bucket_name=bucket_name, prefix=document_key)
        document_bundle.fullUrl = f"DocumentReference/{pmr_document_obj['id']}"
        document_bundle.resource = document(
            document_ref_id=pmr_document_obj["id"],
            document_code=pmr_document_obj["document_type_code"],
            document_display_name=pmr_document_obj["document_type"],
            patient_ref=f"Patient/{patient_obj['id']}",
            document_mime_type=pmr_document_obj["document_mime_type"],
            document_bytes=document_content,
        )
    # Creating Bundle
    bundle = Bundle(
        resource_type="Bundle",
        id=bundle_name,
        type="document",
        timestamp=time_str,
        identifier=identifier,
        entry=[
            practitioner_bundle,
            organization_bundle,
            patient_bundle,
            encounter_bundle,
            appointment_bundle,
            document_bundle,
        ],
    )
    bundle.meta = meta
    print(bundle.json())
    return bundle.json()
