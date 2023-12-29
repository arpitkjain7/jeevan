from fhir.resources.procedure import Procedure
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

subject = {"reference": "Patient/1"}
procedure = Procedure(resource_type="Procedure", subject=subject, status="completed")
meta = Meta(
    profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Procedure"],
)
bundle = Bundle(type="document")
text = {
    "status": "generated",
    "div": '<div xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-IN" lang="en-IN">Assessment of diabetic foot ulcer</div>',
}


code_obj = CodeableConcept()
code_obj.text = "Assessment of diabetic foot ulcer"
code_obj.coding = [
    {
        "system": "http://snomed.info/sct",
        "code": "713130008",
        "display": "Assessment of diabetic foot ulcer",
    }
]
code = code_obj
performedDateTime = "2019-05-12"
followUp_obj = CodeableConcept()
followUp_obj.coding = [
    {
        "system": "http://snomed.info/sct",
        "code": "394725008",
        "display": "Diabetes medication review",
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
