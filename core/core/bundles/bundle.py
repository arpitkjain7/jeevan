from fhir_op_consult_modules import (
    appointment,
    allergyIntolerance,
    condition,
    medical_statement,
    medication_request,
    organization,
    patient,
    practitioner,
    procedure,
    service_request,
    composition,
)
from fhir.resources.identifier import Identifier
from fhir.resources.humanname import HumanName
from fhir.resources.bundle import Bundle, BundleEntry
from fhir.resources.composition import Composition
from fhir.resources.resource import Resource
from fhir.resources.meta import Meta
from datetime import datetime

bundle = Bundle(type="document")
# Set the patient identifier
identifier = Identifier()
identifier.system = "https://example.hospital.com/pr"
identifier.value = "12345"
bundle.identifier = identifier
time_now = datetime.now().astimezone(tz=None).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
meta = Meta(versionId=1, lastUpdated="2015-02-07T13:28:17.239+02:00")
bundle.meta = meta
bundle.timestamp = "2015-02-07T13:28:17.239+02:00"

bundle_entry = BundleEntry()
bundle_entry.resource = bundle
bundle_entry.resource.type = "BundleEntry"

bundle_entry = [
    {
        "fullUrl": "Composition/1",
        "resource": composition(
            practitioner_ref="Practitioner/1",
            practitioner_display="Practitioner 1",
            title="Consultation Report",
            status="final",
            patient_reference="Patient/1",
            patient_display="ABC",
            encounter_reference="Encounter/1",
            custodian_reference="Organization/1",
            custodian_display="UVW Hospital",
        ),
    },
    {
        "fullUrl": "Practitioner/1",
        "resource": practitioner(
            meta_profile="meta profile link",
            identifier_system="https://facility.ndhm.gov.in",
            identifier_value="value",
            identifier_obj_system="obj system",
            identifier_obj_code="identifier code",
            identifier_obj_display="identifier display name",
            practitioner_name="DR. ABC",
        ),
    },
    {
        "fullUrl": "Organization/1",
        "resource": organization(
            identifier_system="https://facility.ndhm.gov.in",
            identifier_value="value",
            meta_profile="profile link",
            identifier_obj_system="obj system",
            identifier_obj_code="identifier code",
            identifier_obj_display="identifier display name",
            org_name="Organization Name",
        ),
    },
    {
        "fullUrl": "Patient/1",
        "resource": patient(
            contact_system="phone",
            contact_value="+91-9876543211",
            contact_use="Home/office",
            patient_dob="1999-12-30",
            patient_gender="male",
            meta_profile="meta profile link",
            identifier_system="https://facility.ndhm.gov.in",
            identifier_value="value",
            identifier_obj_system="obj system",
            identifier_obj_code="identifier code",
            identifier_obj_display="identifier display name",
            patient_name="Patient ABC",
        ),
    },
    {
        "fullUrl": "Encounter/1",
        # need to create function for this
    },
    {
        "fullUrl": "AllergyIntolerance/1",
        "resource": allergyIntolerance(
            text_status="Status",
            text_div="Div",
            coding_system="Clinical status link",
            coding_code="Clinical Status",
            coding_display="Clinical Status",
            verification_system="Verification Status",
            verification_code="Verification Status",
            verification_display="Verification Status",
            codeobj_system="Code",
            codeobj_display="Code",
            codeobj_code="code",
            patient_ref="Patient Reference",
            practitioner_ref="PractitionerRef",
            note_text="Note ",
        ),
    },
    {
        "fullUrl": "Appointment/1",
        "resource": appointment(
            patient_reference="Patient/1",
            practitioner_reference="Practitioner/1",
            snomed_code="abc",
            appt_reason_name="Appointment Reason",
            appt_status="In Progress",
            start_timestamp="2023-05-31T10:00:00Z",
            end_timestamp="2023-06-01T10:00:00Z",
        ),
    },
    {
        "fullUrl": "Condition/1",
        "resource": condition(
            clinical_system="Clinical Status",
            clinical_code="Clinical Status",
            clinical_display="Clinical Status",
            patient_ref="Patient Ref",
            meta_profile="Meta Profile Link",
            text_status="Status",
            text_div="Div",
            codeobj_system="Code",
            codeobj_display="Code",
            codeobj_code="code",
        ),
    },
    {
        "fullUrl": "Procedure/1",
        "resource": procedure(
            patient_ref="Patient Ref",
            code_obj_system="Code",
            code_obj_display="Code",
            code_obj_code="code",
            status="Status",
            procedure_date="2023-06-01T10:00:00Z",
            meta_profile="Meta Profile Link",
            text_status="Status",
            text_div="Div",
            followup_obj_system="Code",
            followup_obj_display="Code",
            followup_obj_code="code",
        ),
    },
    {
        "fullUrl": "ServiceRequest/1",
        "resource": service_request(
            patient_ref="Patient Ref",
            code_obj_system="Code",
            code_obj_display="Code",
            code_obj_code="code",
            status="Status",
            intent="Check-up",
            meta_profile="Meta Profile Link",
            text_status="Status",
            text_div="Div",
            category_obj_system="Code",
            category_obj_display="Code",
            category_obj_code="code",
            code_text="Text",
            practitioner_ref="Dr. ABC/1",
            practitioner_display="Dr. ABC",
            authored_date="2023-06-01T10:00:00Z",
        ),
    },
    {
        "fullUrl": "MedicationStatement/1",
        "resource": medical_statement(
            patient_ref="Patient Ref",
            med_obj_system="Code",
            med_obj_display="med",
            med_obj_code="code",
            status="Status",
            meta_profile="Meta Profile Link",
            text_status="Status",
            text_div="Div",
            date_asserted="2023-06-01T10:00:00Z",
        ),
    },
    {
        "fullUrl": "MedicationRequest/1",
        "resource": medication_request(
            patient_ref="Patient Ref",
            subject_display="Display",
            med_obj_system="Code",
            med_obj_display="med",
            med_obj_code="code",
            intent="Medication",
            status="Status",
            meta_profile="Meta Profile Link",
            text_status="Status",
            text_div="Div",
            category_obj_system="Code",
            category_obj_display="Code",
            category_obj_code="code",
            additional_obj_system="Code",
            additional_obj_display="Code",
            additional_obj_code="code",
            route_system="Code",
            route_display="Code",
            route_code="code",
            practitioner_ref="Dr. ABC/1",
            practitioner_display="Dr. ABC",
        ),
    },
]
print("\n")
bundle.entry = bundle_entry
bundle.type = "document"
bundle_json = bundle.json()
print(bundle_json)
