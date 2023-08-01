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
from fhir.resources.practitionerrole import PractitionerRole
from fhir.resources.procedure import Procedure
from fhir.resources.servicerequest import ServiceRequest
from fhir.resources.composition import Composition, CompositionSection
from fhir.resources.humanname import HumanName
from fhir.resources.identifier import Identifier
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.dosage import Dosage
from fhir.resources.reference import Reference
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.codeablereference import CodeableReference
from fhir.resources.reference import Reference
from fhir.resources.meta import Meta
from datetime import datetime
import pytz

timezone = pytz.timezone("Asia/Kolkata")

time_now = datetime.now().astimezone(tz=None).strftime("%Y-%m-%dT%H:%M:%S.%f%z")

time_now = datetime.now().astimezone(tz=None).strftime("%Y-%m-%dT%H:%M:%S.%f%z")


def patient(
    patient_id: str,
    patient_mobile_number: str,
    patient_dob: str,
    patient_gender: str,
    patient_abha_id: str,
    patient_name: str,
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
    identifier.system = "https://healthid.ndhm.gov.in"
    identifier.value = patient_abha_id
    codeable_obj = CodeableConcept()
    codeable_obj.coding = [
        {
            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
            "code": "MR",
            "display": "Medical record number",
        }
    ]
    identifier.type = codeable_obj
    patient.identifier = [identifier]
    patient.meta = meta
    name = HumanName()
    name.text = patient_name
    patient.name = [name]
    contact_point = ContactPoint(system="phone", value=patient_mobile_number)
    # contact_point = {
    #     "system": "phone",
    #     "value": patient_mobile_number,
    # }
    patient.telecom = [contact_point]
    patient.gender = patient_gender
    patient.birthDate = patient_dob
    patient_json = patient.json()
    print(patient_json)
    return patient


def encounter(
    encounter_id: str,
    encounter_type_code: str,
    encounter_type_display: str,
    encounter_start: str,
    encounter_end: str,
    patient_reference: str,
):
    print("Inside encounter")
    encounter = Encounter(resource_type="Encounter", id=encounter_id, status="finished")
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
    identifier.system = "https://ndhm.in"
    identifier.value = "S100"
    encounter.identifier = [identifier]
    patient_ref = Reference()
    patient_ref.reference = patient_reference
    encounter.subject = patient_ref
    encounter.actualPeriod = Period(start=encounter_start, end=encounter_end)
    encounter_json = encounter.json()
    print(encounter_json)
    return encounter


## serviceType and appointmentType needs to be figured out
def appointment(
    patient_ref: str,
    practitioner_ref: str,
    status: str,
    start_timestamp: str,
    end_timestamp: str,
):
    print("Inside Appointment")
    meta = Meta(
        profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Appointment"],
    )
    patient_reference = Reference()
    patient_reference.reference = patient_ref
    practitioner_reference = Reference()
    practitioner_reference.reference = practitioner_ref
    # Create an Appointment instance
    appointment = Appointment(
        status=status,
        participant=[
            AppointmentParticipant(actor=patient_reference, status="accepted"),
            AppointmentParticipant(actor=practitioner_reference, status="accepted"),
        ],
    )

    appointment.meta = meta
    appointment.status = status
    appointment.start = start_timestamp  # Replace with actual start time
    appointment.end = end_timestamp  # Replace with actual end time
    print(appointment.json())
    return appointment


def practitioner(
    practitioner_id: str, medical_licence_number: str, practitioner_name: str
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
    identifier.system = "https://doctor.ndhm.gov.in"
    identifier.value = medical_licence_number
    codeable_obj = CodeableConcept()
    codeable_obj.coding = [
        {
            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
            "code": "MD",
            "display": "Medical License number",
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
    return practitioner


def practitioner_role(
    practitioner_id: str,
    identifier_value: str,
    identifier_code: str,
    identifier_display_value: str,
    practitioner_ref: str,
    practitioner_display: str,
    organization_ref: str,
    codeobj_code: str,
    codeobj_display: str,
):
    print("Inside Practitioner Role")
    practitioner_role = PractitionerRole(
        resource_type="PractitionerRole", id=practitioner_id
    )
    meta = Meta(
        profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/PractitionerRole"],
    )
    identifier = Identifier()
    identifier.system = "http://snomed.info/sct"
    identifier.value = identifier_value
    codeable_obj = CodeableConcept()
    codeable_obj.coding = [
        {
            "system": "http://snomed.info/sct",
            "code": identifier_code,
            "display": identifier_display_value,
        }
    ]
    identifier.type = codeable_obj
    practitioner_role.identifier = [identifier]
    code = CodeableConcept()
    code.coding = [
        {
            "system": "http://snomed.info/sct",
            "code": codeobj_code,
            "display": codeobj_display,
        }
    ]

    practitioner_role.practitioner = Reference(
        reference=f"Practitioner/{practitioner_ref}", display=practitioner_display
    )

    practitioner_role.organization = Reference(
        reference=f"Organization/{organization_ref}"
    )
    practitioner_role.meta = meta
    practitioner_role.code = [code]
    practitioner_role_json = practitioner_role.json()
    print(practitioner_role_json)
    return practitioner_role


def organization(
    organization_id: str,
    organization_prn: str,
    organization_name: str,
    organization_phone_number: str = None,
    organization_email_id: str = None,
):
    print("Inside Org")
    organization = Organization(resource_type="Organization", id=organization_id)
    meta = Meta(
        profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Organization"],
    )
    identifier = Identifier()
    identifier.system = "https://facility.ndhm.gov.in"
    identifier.value = organization_prn
    codeable_obj = CodeableConcept()
    codeable_obj.coding = [
        {
            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
            "code": "PRN",
            "display": "Provider number",
        }
    ]
    identifier.type = codeable_obj
    organization.identifier = [identifier]
    organization.meta = meta
    organization.name = organization_name
    # TODO: COnvert into json
    # contact_details = []
    # if organization_phone_number:
    #     contact_phone = ContactPoint()
    #     contact_phone.system = "phone"
    #     contact_phone.value = organization_phone_number
    #     contact_details.append(contact_phone)
    # if organization_email_id:
    #     contact_email = ContactPoint()
    #     contact_email.system = "email"
    #     contact_email.value = organization_email_id
    #     contact_details.append(contact_email)
    # if len(contact_details) > 0:
    #     organization.contact = contact_details
    organization_json = organization.json()
    print(organization_json)
    return organization


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
        subject={"reference": patient_ref},
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
    return document_reference


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
    return condition_obj


# TODO: observation (Observation resource represents an individual laboratory test  )


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
    return allergyIntolerance


def procedure(
    patient_ref: str,
    procedure_id: str,
    code_obj_code: str,
    code_obj_display: str,
    status: str,
    followup_obj_code: str,
    followup_obj_display: str,
):
    print("Inside Procedure")
    subject = {"reference": f"Patient/{patient_ref}"}
    procedure = Procedure(resource_type="Procedure", subject=subject, status=status)
    meta = Meta(
        profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Procedure"],
    )
    code = CodeableConcept()
    code.text = "Assessment of diabetic foot ulcer"
    code.coding = [
        {
            "system": "http://snomed.info/sct",
            "code": code_obj_code,
            "display": code_obj_display,
        }
    ]
    # performedDateTime = procedure_date
    followUp_obj = CodeableConcept()
    followUp_obj.coding = [
        {
            "system": "http://snomed.info/sct",
            "code": followup_obj_code,
            "display": followup_obj_display,
        }
    ]
    procedure.meta = meta
    procedure.id = procedure_id
    procedure.code = code
    procedure.subject = subject
    procedure.followUp = [followUp_obj]
    # procedure.date
    # Convert the Patient resource to JSON
    procedure_json = procedure.json()
    print(procedure_json)
    return procedure


# TODO : FamilyMemberHistory
def service_request(
    patient_ref: str,
    code_obj_code: str,
    code_obj_display: str,
    status: str,
    intent: str,
    service_request_id: str,
    category_obj_code: str,
    category_obj_display: str,
    code_text: str,
    practitioner_ref: str,
    practitioner_display: str,
    authored_date: str,
):
    print("Inside Service Req")
    subject = {"reference": f"Patient{patient_ref}"}
    serviceReq = ServiceRequest(
        resource_type="ServiceRequest",
        subject=subject,
        status=status,
        intent=intent,
    )
    meta = Meta(
        profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/ServiceRequest"],
    )
    requestor = {
        "reference": f"Practitioner/{practitioner_ref}",
        "display": practitioner_display,
    }
    category_obj = CodeableConcept()
    category_obj.coding = [
        {
            "system": "http://snomed.info/sct",
            "code": category_obj_code,
            "display": category_obj_display,
        }
    ]
    category = category_obj
    code_obj = CodeableConcept()
    code_obj.coding = [
        {
            "system": "http://snomed.info/sct",
            "code": code_obj_code,
            "display": code_obj_display,
        }
    ]
    code_obj.text = code_text
    code = (
        CodeableReference()
    )  # this CODE part need to be checked furhter, Codeable concept and codeable Reference
    code.concept = code_obj
    authored = authored_date
    serviceReq.meta = meta
    serviceReq.id = service_request_id
    serviceReq.code = code
    serviceReq.subject = subject
    serviceReq.authoredOn = authored
    serviceReq.requester = requestor
    serviceReq.category = [category]
    # Convert the Patient resource to JSON
    serviceReq_json = serviceReq.json()
    print(serviceReq_json)
    return serviceReq


def medical_statement(
    patient_ref: str,
    medication_obj_code: str,
    medication_obj_display: str,
    status: str,
    medication_statement_id: str,
):
    print("Inside Medical Statement")
    subject = {"reference": patient_ref}
    medication_obj = CodeableConcept()
    medication_obj.coding = [
        {
            "system": "http://snomed.info/sct",
            "code": medication_obj_code,
            "display": medication_obj_display,
        }
    ]
    medication = CodeableReference()  # this CODE part need to be checked furhter
    medication.concept = medication_obj
    medication_statement = MedicationStatement(
        resource_type="MedicationStatement",
        subject=subject,
        status=status,
        medication=medication,
        id=medication_statement_id,
    )
    meta = Meta(
        profile=[
            "https://nrces.in/ndhm/fhir/r4/StructureDefinition/MedicationStatement"
        ],
    )
    medication_statement.meta = meta
    medication_statement.id = medication_statement_id
    medication_statement.subject = subject
    # medication_statement.medicationCodeableConcept = medication_obj
    medication_statement_json = medication_statement.json()
    print(medication_statement_json)
    return medication_statement_json


# medication_request.reasonCode and medication_request.reasonReference
# medication vs medicationCodeableConcept
def medication_request(
    patient_ref: str,
    subject_display: str,
    medication_obj_code: str,
    medication_obj_display: str,
    status: str,
    intent: str,
    authored_on: str,
    category_obj_code: str,
    category_obj_display: str,
    additional_obj_code: str,
    additional_obj_display: str,
    route_code: str,
    route_display: str,
    practitioner_ref: str,
    practitioner_display: str,
):
    print("Inside Med Request")
    subject = {"reference": f"Patient/{patient_ref}", "display": subject_display}
    medication_obj = CodeableConcept()
    medication_obj.coding = [
        {
            "system": "http://snomed.info/sct",
            "code": medication_obj_code,
            "display": medication_obj_display,
        }
    ]
    medication = CodeableReference()  # this CODE part need to be checked furhter
    medication.concept = medication_obj
    medication_request = MedicationRequest(
        resource_type="MedicationRequest",
        subject=subject,
        status=status,
        intent=intent,
        medication=medication,
    )
    meta = Meta(
        profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/MedicationRequest"],
    )
    category_obj = CodeableConcept()
    category_obj.coding = [
        {
            "system": "http://snomed.info/sct",
            "code": category_obj_code,
            "display": category_obj_display,
        }
    ]
    category = category_obj
    additional_obj = CodeableConcept()
    additional_obj.coding = [
        {
            "system": "http://snomed.info/sct",
            "code": additional_obj_code,
            "display": additional_obj_display,
        }
    ]
    route = CodeableConcept()
    route.coding = [
        {
            "system": "http://snomed.info/sct",
            "code": route_code,
            "display": route_display,
        }
    ]

    dosage = Dosage()
    dosage.additionalInstruction = [additional_obj]
    dosage.route = route
    authored_on = authored_on
    requestor = {
        "reference": f"Practitioner/{practitioner_ref}",
        "display": practitioner_display,
    }
    medication_request.meta = meta
    medication_request.id = "1"
    medication_request.dosageInstruction = [dosage]
    medication_request.subject = subject
    medication_request.category = [category]
    medication_request.authoredOn = authored_on
    medication_request.requester = requestor
    # Convert the Patient resource to JSON
    medication_request_json = medication_request.json()
    print(medication_request_json)
    return medication_request_json
