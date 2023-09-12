from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.humanname import HumanName
from fhir.resources.bundle import Bundle
from fhir.resources.meta import Meta
from fhir.resources.contactdetail import ContactDetail
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.reference import Reference
from datetime import datetime
import json

allergyIntolerance = AllergyIntolerance(
    resource_type="AllergyIntolerance", patient=Reference(reference="Patient/1")
)
meta = Meta(
    profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/AllergyIntolerance"],
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
        "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
        "code": "active",
        "display": "Active",
    }
]
clinicalStatus = codeable_obj
verification_coding_obj = CodeableConcept()
verification_coding_obj.coding = [
    {
        "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
        "code": "confirmed",
        "display": "Confirmed",
    }
]
verificationStatus = verification_coding_obj
code_obj = CodeableConcept()
code_obj.coding = [
    {
        "system": "http://snomed.info/sct",
        "code": "716186003",
        "display": "No known allergy",
    }
]
code = code_obj
patient_ref = Reference()
patient_ref.reference = "Patient/123"
recoder_ref = Reference()
recoder_ref.reference = "Practitioner/1"
note = [{"text": "The patient reports no other known allergy."}]

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
