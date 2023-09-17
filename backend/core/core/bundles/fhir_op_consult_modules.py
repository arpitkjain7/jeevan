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
    patient = Patient(resource_type="Patient", id=patient_id)
    time_str = datetime.now(timezone).isoformat()
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
    return patient_json


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
    practitioner = Practitioner(resource_type="Practitioner")
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
    return practitioner_role_json


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
    return allergy_json


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
    return procedure_json


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
    return serviceReq_json


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
    patient_reference.reference = f"Patient/{patient_ref}"
    practitioner_reference = Reference()
    practitioner_reference.reference = f"Practitioner/{practitioner_ref}"
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
    return appointment.json()


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


# practitioner_role(
#     practitioner_id="12",
#     identifier_value="213",
#     identifier_code="ja",
#     identifier_display_value="jsa",
#     practitioner_ref="112341",
#     practitioner_display="Dr. ABC",
#     organization_ref="Jeevan",
#     codeobj_code="85733003",
#     codeobj_display="General pathologist",
# )


# service_request(
#     patient_ref="1",
#     code_obj_code="16254007",
#     code_obj_display="Lipid Panel",
#     status="Active",
#     intent="order",
#     service_request_id="12",
#     category_obj_code="123",
#     category_obj_display="rew",
#     code_text="Text",
#     practitioner_ref="1",
#     practitioner_display="Dr ABC",
#     authored_date="2020-07-08T09:33:27+07:00",
# )

# procedure(
#     patient_ref="1",
#     procedure_id="3",
#     code_obj_code="36969009",
#     code_obj_display="Placement of stent in coronary artery",
#     status="Active",
#     followup_obj_code="123",
#     followup_obj_display="today",
# )

# medication_request(
#     patient_ref="01",
#     subject_display="RACHIT",
#     medication_obj_code="231",
#     medication_obj_display="Azithromycin",
#     status="active",
#     intent="order",
#     authored_on="2020-07-09",
#     category_obj_code="1213",
#     category_obj_display="Cold",
#     additional_obj_code="3242",
#     additional_obj_display="No ",
#     route_code="2222",
#     route_display="unknown",
#     practitioner_ref="1",
#     practitioner_display="DR. abc",
# )

# appointment(
#     patient_ref="12",
#     practitioner_ref="23",
#     status="accepted",
#     start_timestamp="2020-07-12T09:00:00Z",
#     end_timestamp="2020-07-12T10:00:00Z",
# )


# medical_statement(
#     patient_ref="60",
#     medication_obj_code="23421",
#     medication_obj_display="Dolo",
#     status="active",
#     medication_statement_id="2",
# )

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
#     practitioner_id="wqwe",
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
