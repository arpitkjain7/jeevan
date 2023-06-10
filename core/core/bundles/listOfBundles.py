from fhir.resources.appointment import Appointment, AppointmentParticipant
from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.condition import Condition
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


def allergyIntolerance(
    text_status: str,
    text_div: str,
    coding_system: str,
    coding_code: str,
    coding_display: str,
    verification_system: str,
    verification_code: str,
    verification_display: str,
    codeobj_system: str,
    codeobj_code: str,
    codeobj_display: str,
    patient_ref: str,
    practitioner_ref: str,
    note_text: str,
):
    print("Inside Allergy Intolerance")
    allergyIntolerance = AllergyIntolerance(
        resource_type="AllergyIntolerance", patient=Reference(reference="Patient/1")
    )
    meta = Meta(
        profile=[
            "https://nrces.in/ndhm/fhir/r4/StructureDefinition/AllergyIntolerance"
        ],
    )
    bundle = Bundle(type="document")
    text = {
        "status": text_status,
        "div": text_div,
    }

    codeable_obj = CodeableConcept()
    codeable_obj.coding = [
        {
            "system": coding_system,
            "code": coding_code,
            "display": coding_display,
        }
    ]
    clinicalStatus = codeable_obj
    verification_coding_obj = CodeableConcept()
    verification_coding_obj.coding = [
        {
            "system": verification_system,
            "code": verification_code,
            "display": verification_display,
        }
    ]
    verificationStatus = verification_coding_obj
    code_obj = CodeableConcept()
    code_obj.coding = [
        {
            "system": codeobj_system,
            "code": codeobj_code,
            "display": codeobj_display,
        }
    ]
    code = code_obj
    # patient_ref = Reference()
    # patient_ref.reference = patient_ref
    # recoder_ref = Reference()
    # recoder_ref.reference = practitioner_ref
    note = [{"text": note_text}]

    allergyIntolerance.id = "1"
    allergyIntolerance.meta = meta
    allergyIntolerance.text = text
    allergyIntolerance.clinicalStatus = clinicalStatus
    allergyIntolerance.verificationStatus = verificationStatus
    allergyIntolerance.code = code
    # allergyIntolerance.patient = patient_ref
    allergyIntolerance.recordedDate = "2020-07-09T15:37:31-06:00"
    # recorder is not working
    # "recorder": {
    #  "reference": "Practitioner/1"
    # },
    # allergyIntolerance.recorder
    allergyIntolerance.note = note

    allergy_json = allergyIntolerance.json()
    print(allergy_json)
    return allergy_json


def condition(
    clinical_system: str,
    clinical_code: str,
    clinical_display: str,
    patient_ref: str,
    meta_profile: str,
    text_status: str,
    text_div: str,
    codeobj_system: str,
    codeobj_code: str,
    codeobj_display: str,
):
    print("Inside condition")
    coding_obj = Coding()
    codeable_obj = CodeableConcept()
    codeable_obj.coding = [
        {
            "system": clinical_system,
            "code": clinical_code,
            "display": clinical_display,
        }
    ]
    clinicalStatus = codeable_obj
    subject = {"reference": patient_ref}
    condition = Condition(
        resource_type="Condition", clinicalStatus=clinicalStatus, subject=subject
    )
    meta = Meta(
        profile=[meta_profile],
    )
    # bundle = Bundle(type="document")
    text = {
        "status": text_status,
        "div": text_div,
    }

    code_obj = CodeableConcept()
    code_obj.text = "Foot swelling"
    code_obj.coding = [
        {
            "system": codeobj_system,
            "code": codeobj_code,
            "display": codeobj_display,
        }
    ]
    code = code_obj

    condition.meta = meta
    condition.id = "1"
    condition.text = text
    condition.clinicalStatus = clinicalStatus
    condition.code = code
    condition.subject = subject

    # Convert the Patient resource to JSON
    condition_json = condition.json()
    print(condition_json)
    return condition_json


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


def organization(
    identifier_system: str,
    identifier_value: str,
    meta_profile: str,
    identifier_obj_system: str,
    identifier_obj_code: str,
    identifier_obj_display: str,
    org_name: str,
):
    print("Inside Org")
    organization = Organization(resource_type="Organization")
    meta = Meta(
        profile=[meta_profile],
    )
    bundle = Bundle(type="document")
    identifier = Identifier()
    identifier.system = identifier_system
    identifier.value = identifier_value
    coding_obj = Coding()
    codeable_obj = CodeableConcept()
    codeable_obj.coding = [
        {
            "system": identifier_obj_system,
            "code": identifier_obj_code,
            "display": identifier_obj_display,
        }
    ]
    identifier.type = codeable_obj

    organization.identifier = [identifier]
    organization.meta = meta
    # Set the patient's name
    name = org_name
    organization.name = name
    # contact_point_1 = ContactPoint()
    # contact_point_1 = {
    # "system": "phone",
    # "value": "+91 273 2139 3632",
    # "use": "work"
    # }
    # contact_point_2 = ContactPoint()
    # contact_point_2 = {
    # "system": "email",
    # "value": "contact@facility.uvw.org",
    # "use": "work"
    # }
    # telecom needs to be added
    # organization.telecom = [contact_point_1,contact_point_2]
    # Convert the Patient resource to JSON
    organization_json = organization.json()
    print(organization_json)
    return organization_json


def patient(
    contact_system: str,
    contact_value: str,
    contact_use: str,
    patient_dob: str,
    patient_gender: str,
    meta_profile: str,
    identifier_system: str,
    identifier_value: str,
    identifier_obj_system: str,
    identifier_obj_code: str,
    identifier_obj_display: str,
    patient_name: str,
):
    print("Inside Patient")
    patient = Patient(resource_type="Patient")
    meta = Meta(
        versionId=1,
        lastUpdated="2015-02-07T13:28:17.239+02:00",
        profile=[meta_profile],
    )
    bundle = Bundle(type="document")
    identifier = Identifier()
    identifier.system = identifier_system
    identifier.value = identifier_value
    coding_obj = Coding()
    codeable_obj = CodeableConcept()
    codeable_obj.coding = [
        {
            "system": identifier_obj_system,
            "code": identifier_obj_code,
            "display": identifier_obj_display,
        }
    ]
    identifier.type = codeable_obj

    patient.identifier = [identifier]
    patient.meta = meta
    # Set the patient's name
    name = HumanName()
    name.text = patient_name
    patient.name = [name]
    contact_details = ContactDetail()
    contact_point = ContactPoint()
    contact_point = {
        "system": contact_system,
        "value": contact_value,
        "use": contact_use,
    }
    patient.telecom = [contact_point]
    patient.gender = patient_gender
    patient.birthDate = patient_dob
    # Convert the Patient resource to JSON
    patient_json = patient.json()
    print(patient_json)
    return patient_json


def practitioner(
    meta_profile: str,
    identifier_system: str,
    identifier_value: str,
    identifier_obj_system: str,
    identifier_obj_code: str,
    identifier_obj_display: str,
    practitioner_name: str,
):
    print("Inside Practitioner")
    practitioner = Practitioner(resource_type="Practitioner")
    meta = Meta(
        versionId=1,
        lastUpdated="2015-02-07T13:28:17.239+02:00",
        profile=[meta_profile],
    )
    # bundle = Bundle(type="document")
    identifier = Identifier()
    identifier.system = identifier_system
    identifier.value = identifier_value
    coding_obj = Coding()
    codeable_obj = CodeableConcept()
    codeable_obj.coding = [
        {
            "system": identifier_obj_system,
            "code": identifier_obj_code,
            "display": identifier_obj_display,
        }
    ]
    identifier.type = codeable_obj

    practitioner.identifier = [identifier]
    practitioner.meta = meta
    # Set the patient's name
    name = HumanName()
    name.text = practitioner_name
    practitioner.name = [name]
    # contact_details = ContactDetail()
    # contact_point = ContactPoint()
    # contact_point = {"system": "phone", "value": "8923829323", "use": "home"}
    # patient.telecom = [contact_point]
    # patient.gender = "Male"
    # patient.birthDate = "1992-10-12"
    # Convert the Patient resource to JSON
    practitioner_json = practitioner.json()
    print(practitioner_json)
    return practitioner_json


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


def section(title, coding_system, coding_code, coding_display, reference):
    section = CompositionSection()
    code_obj = CodeableConcept()
    code_obj.coding = [
        {
            "system": coding_system,
            "code": coding_code,
            "display": coding_display,
        }
    ]
    ref = Reference()
    ref.reference = reference
    section.title = title
    section.code = code_obj
    section.entry = [ref]
    return section


def composition(
    practitioner_ref: str,
    practitioner_display: str,
    title: str,
    status: str,
    patient_reference: str,
    patient_display: str,
    encounter_reference: str,
    custodian_reference: str,
    custodian_display: str,
):
    codeable_obj = CodeableConcept()
    codeable_obj.text = "Clinical Consultation report"
    codeable_obj.coding = [
        {
            "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
            "code": "active",
            "display": "Active",
        }
    ]
    author_ref = Reference()
    author_ref.reference = practitioner_ref
    author_ref.display = practitioner_display

    composition = Composition(
        resource_type="Composition",
        id="1",
        date="2020-07-09T15:32:26.605+05:30",
        title=title,
        status=status,
        author=[author_ref],
        type=codeable_obj,
    )
    meta = Meta(
        versionId=1,
        lastUpdated="2015-02-07T13:28:17.239+02:00",
        profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord"],
    )
    bundle = Bundle(type="document")
    text = {
        "status": "generated",
        "div": '<div xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-IN" lang="en-IN">\n      <p>No Known Allergy</p>\n      <p>recordedDate:2015-08-06</p>\n    </div>',
    }
    identifier = Identifier()
    identifier.system = "https://ndhm.in"
    identifier.value = "S100"

    patient_ref = Reference()
    patient_ref.reference = patient_reference
    patient_ref.display = patient_display
    encounter_ref = Reference()
    encounter_ref.reference = encounter_reference
    custodian_ref = Reference()
    custodian_ref.reference = custodian_reference
    custodian_ref.display = custodian_display
    section0 = section(
        "Chief complaints",
        "http://snomed.info/sct",
        "422843007",
        "Chief complaint section",
        "Condition/1",
    )
    section1 = section(
        "Chief complaints",
        "http://snomed.info/sct",
        "422843007",
        "Chief complaint section",
        "Condition/2",
    )
    section2 = section(
        "Chief complaints",
        "http://snomed.info/sct",
        "422843007",
        "Chief complaint section",
        "Condition/3",
    )

    composition.id = "1"
    composition.meta = meta
    composition.text = text
    composition.identifier = [identifier]
    composition.type = codeable_obj
    composition.subject = [patient_ref]
    composition.encounter = encounter_ref
    # composition.date = date
    # recorder is not working
    # "recorder": {
    #  "reference": "Practitioner/1"
    # },
    # allergyIntolerance.recorder
    composition.custodian = custodian_ref
    composition.section = [section0, section1, section2]

    composition_json = composition.json()

    print(composition_json)
    return composition_json


def allergy_intolerance(
    patient_ref: str,
    clinical_system: str,
    clinical_code: str,
    clinical_display: str,
    verification_system: str,
    verification_code: str,
    verification_display: str,
    code_obj_system: str,
    code_obj_code: str,
    code_obj_display: str,
    practitioner_ref: str,
    note_text: str,
):
    allergyIntolerance = AllergyIntolerance(
        resource_type="AllergyIntolerance", patient=Reference(reference=patient_ref)
    )
    meta = Meta(
        profile=[
            "https://nrces.in/ndhm/fhir/r4/StructureDefinition/AllergyIntolerance"
        ],
    )
    bundle = Bundle(type="document")
    text = {
        "status": "generated",
        "div": '<div xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-IN" lang="en-IN">\n      <p>No Known Allergy</p>\n      <p>recordedDate:2015-08-06</p>\n    </div>',
    }

    coding_obj = Coding()
    codeable_obj = CodeableConcept()
    codeable_obj.coding = [
        {
            "system": clinical_system,
            "code": clinical_code,
            "display": clinical_display,
        }
    ]
    clinicalStatus = codeable_obj
    verification_coding_obj = CodeableConcept()
    verification_coding_obj.coding = [
        {
            "system": verification_system,
            "code": verification_code,
            "display": verification_display,
        }
    ]
    verificationStatus = verification_coding_obj
    code_obj = CodeableConcept()
    code_obj.coding = [
        {
            "system": code_obj_system,
            "code": code_obj_code,
            "display": code_obj_display,
        }
    ]
    code = code_obj
    recoder_ref = Reference()
    recoder_ref.reference = practitioner_ref
    note = [{"text": note_text}]

    allergyIntolerance.id = "1"
    allergyIntolerance.meta = meta
    allergyIntolerance.text = text
    allergyIntolerance.clinicalStatus = clinicalStatus
    allergyIntolerance.verificationStatus = verificationStatus
    allergyIntolerance.code = code
    # allergyIntolerance.patient = patient_ref
    allergyIntolerance.recordedDate = "2020-07-09T15:37:31-06:00"
    # recorder is not working
    # "recorder": {
    #  "reference": "Practitioner/1"
    # },
    # allergyIntolerance.recorder
    allergyIntolerance.note = note

    allergy_json = allergyIntolerance.json()

    print(allergy_json)
    return allergy_json
