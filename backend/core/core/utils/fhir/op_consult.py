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
from core.crud.hims_hip_crud import CRUDHIP
from core.crud.hims_appointments_crud import CRUDAppointments
from core.crud.hims_patientDetails_crud import CRUDPatientDetails
from core.crud.hims_docDetails_crud import CRUDDocDetails
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
                entry=[{"reference": document_url}, {"reference": appointment_url}],
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


def opConsultStructured(bundle_name: str, bundle_identifier: str, pmr_id: str):
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
        logging.info(f"{pmr_obj=}")
        # Creating Practitioner Entry
        # pmr_obj = CRUDPatientMedicalRecord().read(pmr_id=pmr_id)
        # pmr_obj = CRUDPatientMedicalRecord().read_details(pmr_id=pmr_id)
        # if len(pmr_obj) > 0:
        #     pmr_obj = pmr_obj[0]
        # logging.info(f"{pmr_obj=}")
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
        # Creating Appointment Entry
        logging.info(f"Creating Appointment Entry")
        appointment_obj = pmr_obj.get("appointment")
        logging.info(f"{appointment_obj=}")
        appointment_bundle = BundleEntry()
        appointment_bundle.fullUrl = f"Appointment/{appointment_obj['id']}"
        appointment_bundle.resource = appointment(
            patient_ref=patient_url,
            practitioner_ref=practitioner_url,
            status=appointment_obj["consultation_status"],
            start_timestamp=encounter_start,
            end_timestamp=encounter_end,
        )
        # Creating Document Entry
        logging.info(f"Creating Document Entry")
        pmr_document_list = CRUDPatientMedicalDocuments().read_by_pmr_id(pmr_id=pmr_id)
        logging.info(f"{pmr_document_list=}")
        document_bundle = BundleEntry()
        for pmr_document_obj in pmr_document_list:
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
            logging.info(f"{document_bundle.resource=}")
        # Creating Composition
        logging.info(f"Creating Composition Entry")
        composition_bundle = BundleEntry()
        composition_bundle.fullUrl = f"Composition/1"
        composition_id = str(uuid.uuid1())
        composition_bundle.resource = composition(
            composition_id=composition_id,
            composition_profile_id="https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord",
            pmr_id=pmr_id,
            patient_ref={"reference": patient_url, "type": "Patient"},
            doctor_ref=[{"reference": practitioner_url}],
            org_ref={"reference": organization_url},
            encounter_ref={"reference": encounter_url, "type": "Encounter"},
            document_ref=document_url,
        )

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
            entry=[
                composition_bundle,
                practitioner_bundle,
                organization_bundle,
                patient_bundle,
                encounter_bundle,
                appointment_bundle,
                document_bundle,
            ],
        )
        bundle.meta = meta
        bundle_dict = bundle.__dict__
        bundle_json = JSONResponse(content=jsonable_encoder(bundle_dict))
        content_bytes = bundle_json.body
        content_str = content_bytes.decode("utf-8")
        response_dict = json.loads(content_str)
        return response_dict
    logging.info(f"No record found for {pmr_id=}")
    return None
