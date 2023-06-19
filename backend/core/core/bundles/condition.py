from fhir.resources.condition import Condition
from fhir.resources.identifier import Identifier
from fhir.resources.humanname import HumanName
from fhir.resources.bundle import Bundle
from fhir.resources.meta import Meta
from fhir.resources.contactdetail import ContactDetail
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from datetime import datetime
import json


coding_obj = Coding()
codeable_obj = CodeableConcept()
codeable_obj.coding = [
    {
        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
        "code": "active",
        "display": "Active",
    }
]
clinicalStatus = codeable_obj
subject = {"reference": "Patient/1"}
condition = Condition(
    resource_type="Condition", clinicalStatus=clinicalStatus, subject=subject
)
meta = Meta(
    profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Condition"],
)
bundle = Bundle(type="document")
text = {
    "status": "generated",
    "div": '<div xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-IN" lang="en-IN">Foot has swollen</div>',
}


code_obj = CodeableConcept()
code_obj.text = "Foot swelling"
code_obj.coding = [
    {
        "system": "http://snomed.info/sct",
        "code": "297142003",
        "display": "Foot swelling",
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
