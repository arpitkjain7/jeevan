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
from core.crud.hims_diagnosis_crud import CRUDDiagnosis
from core.crud.hims_medicalHistory_crud import CRUDMedicalHistory
from core.crud.hims_appointments_crud import CRUDAppointments
from core.crud.hims_patientDetails_crud import CRUDPatientDetails
from core.crud.hims_docDetails_crud import CRUDDocDetails
from core.crud.hims_symptoms_crud import CRUDSymptoms
from core.crud.hims_vitals_crud import CRUDVital
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


def opConsultStructured(bundle_identifier: str, pmr_id: str):
    try:
        logging.info("executing opConsultStructured function")
        ist_timezone = pytz.timezone("Asia/Kolkata")
        current_time_ist = datetime.now(ist_timezone)
        offset_hours = current_time_ist.utcoffset().seconds // 3600
        offset_minutes = (current_time_ist.utcoffset().seconds // 60) % 60
        offset_string = "{:02}:{:02}".format(offset_hours, offset_minutes)
        time_str = current_time_ist.strftime("%Y-%m-%dT%H:%M:%S") + "+" + offset_string
        # time_str = datetime.now(timezone).isoformat()
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
            diagnosis_rec = CRUDDiagnosis().read_by_pmrId(pmr_id=pmr_id)
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
                    "time_str": time_str,
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
                diagnosis=diagnosis_rec[0].get("disease", None),
            )
            bundle_entry_list.append(
                BundleEntry.construct(
                    fullUrl=f"Encounter/{encounter_bundle.id}",
                    resource=encounter_bundle,
                )
            )
            encounter_ref = Reference.construct(
                reference=f"Encounter/{encounter_bundle.id}"
            )
            ref_data.append(encounter_ref)

            # Creating ChiefComplaint/Conditions
            logging.info(f"Creating ChiefComplaint/Conditions Entry")
            sympt_list = CRUDSymptoms().read_by_pmrId(pmr_id=pmr_id)
            logging.info(f"{sympt_list=}")
            condition_sections = [
                get_condition_construct(
                    condition_id=str(uuid.uuid4()),
                    clinical_display=sympt_obj["symptom"],
                    patient_ref=patient_ref_id,
                    encounter_ref=encounter_ref_id,
                    condition_type="COMPLAIN",
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

            # Creating Medical History
            logging.info(f"Creating Medical History Entry")
            med_history_list = CRUDMedicalHistory().read_by_pmrId(pmr_id=pmr_id)
            logging.info(f"{med_history_list=}")
            med_his_sections = [
                get_condition_construct(
                    condition_id=str(uuid.uuid4()),
                    clinical_display=med_history_obj["medical_history"],
                    patient_ref=patient_ref_id,
                    encounter_ref=encounter_ref_id,
                    condition_type="HISTORY",
                )
                for med_history_obj in med_history_list
            ]
            bundle_entry_list.extend(
                [
                    BundleEntry.construct(
                        fullUrl=f"Condition/{med_his_bundle.id}",
                        resource=med_his_bundle,
                    )
                    for med_his_bundle in med_his_sections
                ]
            )
            ref_data.extend(med_his_sections)
            codeable_obj = CodeableConcept()
            codeable_obj.coding = [
                {
                    "system": "http://snomed.info/sct",
                    "code": "371529009",
                    "display": "History and physical report",
                }
            ]
            med_his_entry = [
                Reference.construct(reference=f"Condition/{section.id}")
                for section in med_his_sections
            ]
            med_his_ref = {
                "title": "Medical History",
                "entry": med_his_entry,
                "code": codeable_obj,
            }
            section_refs.append(med_his_ref)

            # Creating physical examination
            physical_examination_bundle_list = []
            logging.info(f"Creating Vitals Entry")
            vital_obj = CRUDVital().read_by_pmrId(pmr_id=pmr_id)
            physical_examination = f"Temperature {vital_obj['body_temperature']} Blood Pressure {vital_obj['systolic_blood_pressure']}/{vital_obj['diastolic_blood_pressure']}"
            physical_examination_temp_bundle = get_observation_construct(
                observation_id=str(uuid.uuid4()),
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
                    fullUrl=f"Observation/{physical_examination_temp_bundle.id}",
                    resource=physical_examination_temp_bundle,
                )
            )
            physical_examination_sbp_bundle = get_observation_construct(
                observation_id=str(uuid.uuid4()),
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
                    fullUrl=f"Observation/{physical_examination_sbp_bundle.id}",
                    resource=physical_examination_sbp_bundle,
                )
            )

            physical_examination_dbp_bundle = get_observation_construct(
                observation_id=str(uuid.uuid4()),
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
                    fullUrl=f"Observation/{physical_examination_dbp_bundle.id}",
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
                    reference=f"Observation/{physical_examination_bundle.id}"
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
            composition_meta = Meta(
                versionId=1,
                lastUpdated=time_str,
                profile=[
                    "https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord"
                ],
            )
            composition = Composition.construct(
                id=str(uuid.uuid4()),
                title="Consultation Report",
                date=slot_obj["date"],
                status="final",  # final | amended | entered-in-error | preliminary,
                type=CodeableConcept.construct(
                    text="Clinical consultation report",
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
                meta=composition_meta,
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
            bundle.id = bundle_identifier
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
