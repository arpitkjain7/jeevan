from fhir.resources.appointment import Appointment, AppointmentParticipant
from fhir.resources.encounter import Encounter
from fhir.resources.documentreference import DocumentReference, DocumentReferenceContent
from fhir.resources.attachment import Attachment
from fhir.resources.period import Period
from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.condition import Condition, ConditionStage
from fhir.resources.medicationstatement import MedicationStatement
from fhir.resources.medicationrequest import MedicationRequest
from fhir.resources.organization import Organization
from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.procedure import Procedure
from fhir.resources.servicerequest import ServiceRequest
from fhir.resources.composition import Composition, CompositionSection
from fhir.resources.humanname import HumanName
from fhir.resources.identifier import Identifier
from fhir.resources.contactdetail import ContactDetail
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.dosage import Dosage
from fhir.resources.bundle import Bundle
from fhir.resources.reference import Reference
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.codeablereference import CodeableReference
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference
from fhir.resources.meta import Meta
from datetime import datetime
import pytz

timezone = pytz.timezone("Asia/Kolkata")

time_now = datetime.now().astimezone(tz=None).strftime("%Y-%m-%dT%H:%M:%S.%f%z")

time_now = datetime.now().astimezone(tz=None).strftime("%Y-%m-%dT%H:%M:%S.%f%z")


def appointment(
    patient_reference: str,
    practitioner_reference: str,
    snomed_code: str,
    appt_reason_name: str,
    appt_status: str,
    start_timestamp: str,
    end_timestamp: str,
):
    # Create a reference to the patient
    print("Inside Appointment")
    patient_ref = Reference()
    patient_ref.reference = patient_reference  # Replace with actual patient ID

    # Create a reference to the practitioner
    practitioner_ref = Reference()
    practitioner_ref.reference = (
        practitioner_reference  # Replace with actual practitioner ID
    )

    # Create a Coding instance for the SNOMED CT code
    snomed_coding = Coding()
    snomed_coding.system = "http://snomed.info/sct"
    snomed_coding.code = snomed_code  # Replace with actual SNOMED CT code
    snomed_coding.display = appt_reason_name  # Replace with actual reason name

    # Create a CodeableConcept instance for the reason
    appointment_reason = CodeableConcept()
    appointment_reason.coding = [snomed_coding]

    # Create an Appointment instance
    appointment = Appointment(
        status=appt_status,
        participant=[
            AppointmentParticipant(actor=patient_ref, status="accepted"),
            AppointmentParticipant(actor=practitioner_ref, status="accepted"),
        ],
    )
    appointment.start = start_timestamp  # Replace with actual start time
    appointment.end = end_timestamp  # Replace with actual end time
    print(appointment.json())
    return appointment.json()


def medical_statement(
    patient_ref: str,
    med_obj_system: str,
    med_obj_code: str,
    med_obj_display: str,
    status: str,
    meta_profile: str,
    text_status: str,
    text_div: str,
    date_asserted: str,
):
    print("Inside Medical Statement")
    subject = {"reference": patient_ref}
    med_obj = CodeableConcept()
    med_obj.coding = [
        {
            "system": med_obj_system,
            "code": med_obj_code,
            "display": med_obj_display,
        }
    ]
    med = CodeableReference()  # this CODE part need to be checked furhter
    med.concept = med_obj
    medicationStatement = MedicationStatement(
        resource_type="MedicationStatement",
        subject=subject,
        status=status,
        medication=med,
    )
    meta = Meta(
        profile=[meta_profile],
    )
    bundle = Bundle(type="document")
    text = {
        "status": text_status,
        "div": text_div,
    }
    medicationStatement.meta = meta
    medicationStatement.id = "1"
    medicationStatement.text = text
    medicationStatement.subject = subject
    medicationStatement.dateAsserted = date_asserted
    # Convert the Patient resource to JSON
    procedure_json = medicationStatement.json()
    print(procedure_json)
    return procedure_json


def medication_request(
    patient_ref: str,
    subject_display: str,
    med_obj_system: str,
    med_obj_code: str,
    med_obj_display: str,
    status: str,
    intent: str,
    meta_profile: str,
    text_status: str,
    text_div: str,
    category_obj_system: str,
    category_obj_code: str,
    category_obj_display: str,
    additional_obj_system: str,
    additional_obj_code: str,
    additional_obj_display: str,
    route_system: str,
    route_code: str,
    route_display: str,
    practitioner_ref: str,
    practitioner_display: str,
):
    print("Inside Med Request")
    subject = {"reference": patient_ref, "display": subject_display}
    med_obj = CodeableConcept()
    med_obj.coding = [
        {
            "system": med_obj_system,
            "code": med_obj_code,
            "display": med_obj_display,
        }
    ]
    med = CodeableReference()  # this CODE part need to be checked furhter
    med.concept = med_obj
    medicationReq = MedicationRequest(
        resource_type="MedicationRequest",
        subject=subject,
        status=status,
        intent=intent,
        medication=med,
    )
    meta = Meta(
        profile=[meta_profile],
    )
    bundle = Bundle(type="document")
    text = {
        "status": text_status,
        "div": text_div,
    }
    category_obj = CodeableConcept()
    category_obj.coding = [
        {
            "system": category_obj_system,
            "code": category_obj_code,
            "display": category_obj_display,
        }
    ]
    category = category_obj
    additional_obj = CodeableConcept()
    additional_obj.coding = [
        {
            "system": additional_obj_system,
            "code": additional_obj_code,
            "display": additional_obj_display,
        }
    ]
    route = CodeableConcept()
    route.coding = [
        {
            "system": route_system,
            "code": route_code,
            "display": route_display,
        }
    ]

    dosage = Dosage()
    dosage.additionalInstruction = [additional_obj]
    dosage.route = route
    authored = "2020-07-09"
    requestor = {"reference": practitioner_ref, "display": practitioner_display}
    medicationReq.meta = meta
    medicationReq.id = "1"
    medicationReq.text = text
    medicationReq.dosageInstruction = [dosage]
    medicationReq.subject = subject
    medicationReq.authoredOn = authored
    medicationReq.requester = requestor
    # Convert the Patient resource to JSON
    procedure_json = medicationReq.json()
    print(procedure_json)
    return procedure_json


def procedure(
    patient_ref: str,
    code_obj_system: str,
    code_obj_code: str,
    code_obj_display: str,
    status: str,
    procedure_date: str,
    meta_profile: str,
    text_status: str,
    text_div: str,
    followup_obj_system: str,
    followup_obj_code: str,
    followup_obj_display: str,
):
    print("Inside Procedure")
    subject = {"reference": patient_ref}
    procedure = Procedure(resource_type="Procedure", subject=subject, status=status)
    meta = Meta(
        profile=[meta_profile],
    )
    bundle = Bundle(type="document")
    text = {
        "status": text_status,
        "div": text_div,
    }

    code_obj = CodeableConcept()
    code_obj.text = "Assessment of diabetic foot ulcer"
    code_obj.coding = [
        {
            "system": code_obj_system,
            "code": code_obj_code,
            "display": code_obj_display,
        }
    ]
    code = code_obj
    performedDateTime = procedure_date
    followUp_obj = CodeableConcept()
    followUp_obj.coding = [
        {
            "system": followup_obj_system,
            "code": followup_obj_code,
            "display": followup_obj_display,
        }
    ]

    procedure.meta = meta
    procedure.id = "1"
    procedure.text = text
    procedure.code = code
    procedure.subject = subject
    procedure.followUp = [followUp_obj]
    # Convert the Patient resource to JSON
    procedure_json = procedure.json()
    print(procedure_json)
    return procedure_json


def service_request(
    patient_ref: str,
    code_obj_system: str,
    code_obj_code: str,
    code_obj_display: str,
    status: str,
    intent: str,
    meta_profile: str,
    text_status: str,
    text_div: str,
    category_obj_system: str,
    category_obj_code: str,
    category_obj_display: str,
    code_text: str,
    practitioner_ref: str,
    practitioner_display: str,
    authored_date: str,
):
    print("Inside Service Req")
    subject = {"reference": patient_ref}
    serviceReq = ServiceRequest(
        resource_type="ServiceRequest",
        subject=subject,
        status=status,
        intent=intent,
    )
    meta = Meta(
        profile=[meta_profile],
    )
    bundle = Bundle(type="document")
    text = {"status": text_status, "div": text_div}
    category_obj = CodeableConcept()
    category_obj.coding = [
        {
            "system": category_obj_system,
            "code": category_obj_code,
            "display": category_obj_display,
        }
    ]
    category = category_obj
    code_obj = CodeableConcept()
    code_obj.coding = [
        {
            "system": code_obj_system,
            "code": code_obj_code,
            "display": code_obj_display,
        }
    ]
    code_obj.text = code_text
    code = CodeableReference()  # this CODE part need to be checked furhter
    code.concept = code_obj
    authored = authored_date
    requestor = {"reference": practitioner_ref, "display": practitioner_display}
    serviceReq.meta = meta
    serviceReq.id = "1"
    serviceReq.text = text
    serviceReq.code = code
    serviceReq.subject = subject
    serviceReq.authoredOn = authored
    serviceReq.requester = requestor
    serviceReq.category = [category]
    # Convert the Patient resource to JSON
    serviceReq_json = serviceReq.json()
    print(serviceReq_json)
    return serviceReq_json


##########################################################################
def patient(
    patient_id: str,
    patient_mobile_number: str,
    patient_dob: str,
    patient_gender: str,
    identifier_system: str,
    identifier_value: str,
    identifier_code_system: str,
    identifier_code: str,
    identifier_display_value: str,
    patient_name: str,
    patient_address: str = None,
):
    print("Inside Patient")
    patient = Patient(resource_type="Patient", id=patient_id)
    time_str = datetime.now(timezone).isoformat()
    print(time_str)
    meta = Meta(
        versionId=1,
        lastUpdated=time_str,
        profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Patient"],
    )
    identifier = Identifier()
    identifier.system = identifier_system
    identifier.value = identifier_value
    codeable_obj = CodeableConcept()
    codeable_obj.coding = [
        {
            "system": identifier_code_system,
            "code": identifier_code,
            "display": identifier_display_value,
        }
    ]
    identifier.type = codeable_obj
    patient.identifier = [identifier]
    patient.meta = meta
    name = HumanName()
    name.text = patient_name
    patient.name = [name]
    contact_point = ContactPoint()
    contact_point = {
        "system": "phone",
        "value": patient_mobile_number,
    }
    patient.telecom = [contact_point]
    patient.gender = patient_gender
    patient.birthDate = patient_dob
    patient.address = patient_address
    patient_json = patient.json()
    print(patient_json)
    return patient_json


def practitioner(
    practitioner_id: str,
    identifier_system: str,
    identifier_value: str,
    identifier_code_system: str,
    identifier_code: str,
    identifier_display_value: str,
    practitioner_name: str,
):
    print("Inside Practitioner")
    practitioner = Practitioner(resource_type="Practitioner", id=practitioner_id)
    time_str = datetime.now(timezone).isoformat()
    meta = Meta(
        versionId=1,
        lastUpdated=time_str,
        profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Practitioner"],
    )
    identifier = Identifier()
    identifier.system = identifier_system
    identifier.value = identifier_value
    codeable_obj = CodeableConcept()
    codeable_obj.coding = [
        {
            "system": identifier_code_system,
            "code": identifier_code,
            "display": identifier_display_value,
        }
    ]
    identifier.type = codeable_obj
    practitioner.identifier = [identifier]
    practitioner.meta = meta
    name = HumanName()
    name.text = practitioner_name
    practitioner.name = [name]
    practitioner_json = practitioner.json()
    print(practitioner_json)
    return practitioner_json


def encounter(
    encounter_id: str,
    encounter_status: str,
    encounter_type_code: str,
    encounter_type_display: str,
    encounter_start: str,
    encounter_end: str,
    patient_reference: str,
    identifier_system: str,
    identifier_value: str,
):
    print("Inside encounter")
    encounter = Encounter(
        resource_type="Encounter", id=encounter_id, status=encounter_status
    )
    time_str = datetime.now(timezone).isoformat()
    meta = Meta(
        versionId=1,
        lastUpdated=time_str,
        profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Encounter"],
    )
    encounter.meta = meta
    codeable_obj = CodeableConcept()
    codeable_obj.coding = [
        {
            "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
            "code": encounter_type_code,
            "display": encounter_type_display,
        }
    ]
    encounter.class_fhir = [codeable_obj]
    identifier = Identifier()
    identifier.system = identifier_system
    identifier.value = identifier_value
    encounter.identifier = [identifier]
    patient_ref = Reference()
    patient_ref.reference = patient_reference
    encounter.subject = patient_ref
    encounter.actualPeriod = Period(start=encounter_start, end=encounter_end)
    encounter_json = encounter.json()
    print(encounter_json)
    return encounter_json


# TODO: pending
def practitioner_role(
    practitioner_id: str,
    identifier_system: str,
    identifier_value: str,
    identifier_code_system: str,
    identifier_code: str,
    identifier_display_value: str,
    practitioner_name: str,
):
    print("Inside Practitioner Role")
    practitioner = Practitioner(resource_type="Practitioner", id=practitioner_id)
    time_str = datetime.now(timezone).isoformat()
    meta = Meta(
        versionId=1,
        lastUpdated=time_str,
        profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/PractitionerRole"],
    )
    identifier = Identifier()
    identifier.system = identifier_system
    identifier.value = identifier_value
    codeable_obj = CodeableConcept()
    codeable_obj.coding = [
        {
            "system": identifier_code_system,
            "code": identifier_code,
            "display": identifier_display_value,
        }
    ]
    identifier.type = codeable_obj
    practitioner.identifier = [identifier]
    practitioner.meta = meta
    name = HumanName()
    name.text = practitioner_name
    practitioner.name = [name]
    practitioner_json = practitioner.json()
    print(practitioner_json)
    return practitioner_json


def organization(
    org_id: str,
    identifier_system: str,
    identifier_value: str,
    identifier_code_system: str,
    identifier_code: str,
    identifier_display_value: str,
    org_name: str,
    org_phone_number: str,
    org_email_id: str,
):
    print("Inside Org")
    organization = Organization(resource_type="Organization", id=org_id)
    meta = Meta(
        profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Organization"],
    )
    identifier = Identifier()
    identifier.system = identifier_system
    identifier.value = identifier_value
    codeable_obj = CodeableConcept()
    codeable_obj.coding = [
        {
            "system": identifier_code_system,
            "code": identifier_code,
            "display": identifier_display_value,
        }
    ]
    identifier.type = codeable_obj
    organization.identifier = [identifier]
    organization.meta = meta
    name = org_name
    organization.name = name
    # TODO: COnvert into json
    # contact_phone = ContactPoint()
    # contact_phone.system = "phone"
    # contact_phone.value = org_phone_number
    # contact_email = ContactPoint()
    # contact_email.system = "email"
    # contact_email.value = org_email_id
    # organization = [contact_phone, contact_email]
    # Convert the Patient resource to JSON
    organization_json = organization.json()
    print(organization_json)
    return organization_json


# TODO: observation
def condition(
    condition_id: str,
    clinical_system: str,
    clinical_code: str,
    clinical_display: str,
    patient_ref: str,
    encounter_ref: str,
):
    print("Inside condition")
    clinicalStatus_codeable_obj = CodeableConcept()
    clinicalStatus_codeable_obj.coding = [
        {
            "system": clinical_system,
            "code": "active",
            "display": "active",
        }
    ]
    condition_obj = Condition(
        resource_type="Condition",
        id=condition_id,
        clinicalStatus=clinicalStatus_codeable_obj,
        subject={"reference": f"Patient/{patient_ref}"},
    )
    codeable_obj = CodeableConcept()
    codeable_obj.coding = [
        {
            "system": clinical_system,
            "code": clinical_code,
            "display": clinical_display,
        }
    ]
    codeable_obj.text = clinical_display
    encounter = {"reference": f"Encounter/{encounter_ref}"}
    meta = Meta(
        profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Condition"],
    )
    condition_obj.meta = meta
    condition_obj.code = codeable_obj
    condition_obj.encounter = encounter
    # Convert the Patient resource to JSON
    condition_json = condition_obj.json()
    print(condition_json)
    return condition_json


def document(
    document_ref_id: str,
    document_code: str,
    document_display_name: str,
    patient_ref: str,
    document_mime_type: str,
    document_bytes: str,
):
    print("Inside document")
    attachment_obj = Attachment(
        contentType=document_mime_type, language="en-IN", data=document_bytes
    )
    document_ref_obj = DocumentReferenceContent(attachment=attachment_obj)
    document_reference = DocumentReference(
        resource_type="DocumentReference",
        id=document_ref_id,
        status="current",
        docStatus="final",
        subject={"reference": f"Patient/{patient_ref}"},
        content=[document_ref_obj],
    )
    time_str = datetime.now(timezone).isoformat()
    meta = Meta(
        versionId=1,
        lastUpdated=time_str,
        profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/DocumentReference"],
    )
    document_reference.meta = meta
    codeable_obj = CodeableConcept()
    codeable_obj.coding = [
        {
            "system": "http://snomed.info/sct",
            "code": document_code,
            "display": document_display_name,
        }
    ]
    codeable_obj.text = document_display_name
    document_reference.type = codeable_obj
    document_reference_json = document_reference.json()
    print(document_reference_json)
    return document_reference_json


def allergyIntolerance(
    allergyIntolerance_id: str,
    codeobj_code: str,
    codeobj_display: str,
    patient_ref: str,
):
    print("Inside Allergy Intolerance")
    allergyIntolerance = AllergyIntolerance(
        resource_type="AllergyIntolerance",
        patient=Reference(reference=f"Patient/{patient_ref}"),
        id=allergyIntolerance_id,
    )
    meta = Meta(
        profile=[
            "https://nrces.in/ndhm/fhir/r4/StructureDefinition/AllergyIntolerance"
        ],
    )
    code_obj = CodeableConcept()
    code_obj.coding = [
        {
            "system": "http://snomed.info/sct",
            "code": codeobj_code,
            "display": codeobj_display,
        }
    ]
    code_obj.text = codeobj_display
    code = code_obj
    allergyIntolerance.meta = meta
    allergyIntolerance.code = code
    allergy_json = allergyIntolerance.json()
    print(allergy_json)
    return allergy_json


# allergyIntolerance(
#     allergyIntolerance_id="1",
#     codeobj_code="716186003",
#     codeobj_display="test",
#     patient_ref="60",
# )

# document(
#     document_ref_id="1",
#     document_code="2324",
#     document_display_name="prescription",
#     patient_ref="4",
#     document_mime_type="application/pdf",
#     document_bytes="werwerwe",
# )
# condition(
#     condition_id="1",
#     clinical_system="http://snomed.info/sct",
#     clinical_code="12312",
#     clinical_display="sdfsd",
#     patient_id="2",
#     encounter_id="5",
# )
# organization(
#     org_id="1",
#     identifier_system="https://facility.ndhm.gov.in",
#     identifier_value="4567878",
#     identifier_code_system="http://terminology.hl7.org/CodeSystem/v2-0203",
#     identifier_code="PRN",
#     identifier_display_value="Provider number",
#     org_name="ABC HealthCare",
#     org_phone_number="2345234234",
#     org_email_id="sdfsdf",
# )

# practitioner(
#     identifier_system="https://doctor.ndhm.gov.in",
#     identifier_value="ABC",
#     identifier_code_system="http://terminology.hl7.org/CodeSystem/v2-0203",
#     identifier_code="MD",
#     identifier_display_value="Medical License number",
#     practitioner_name="Dr. Arpit Jain",
# )

# patient(
#     patient_id="1",
#     patient_dob="1992-12-10",
#     patient_mobile_number="9775656787",
#     patient_gender="Male",
#     patient_name="Arpit",
#     identifier_system="https://healthid.ndhm.gov.in",
#     identifier_value="asdasd",
#     identifier_code_system="http://terminology.hl7.org/CodeSystem/v2-0203",
#     identifier_code="MR",
#     identifier_display_value="Medical record number",
# )

# encounter(
#     encounter_id="1",
#     encounter_status="finished",
#     encounter_type_code="AMB",
#     encounter_type_display="ambulatory",
#     encounter_start="2015-02-07T13:28:17.239+02:00",
#     encounter_end="2015-02-07T13:28:17.239+02:00",
#     patient_reference="Patient/1",
#     identifier_system="https://healthid.ndhm.gov.in",
#     identifier_value="acds",
# )
