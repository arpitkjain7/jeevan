from fhir.resources.servicerequest import ServiceRequest
from fhir.resources.identifier import Identifier
from fhir.resources.reference import Reference
from fhir.resources.bundle import Bundle
from fhir.resources.meta import Meta
from fhir.resources.codeablereference import CodeableReference
from fhir.resources.codeableconcept import CodeableConcept
from datetime import datetime
import json

subject = {"reference": "Patient/1"}
serviceReq = ServiceRequest(
    resource_type="ServiceRequest",
    subject=subject,
    status="active",
    intent="order",
)
meta = Meta(
    profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/ServiceRequest"],
)
bundle = Bundle(type="document")
text = {
    "status": "generated",
    "div": '<div xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-IN" lang="en-IN">Service Request for fasting lipid profile</div>',
}
category_obj = CodeableConcept()
category_obj.coding = [
    {
        "system": "http://snomed.info/sct",
        "code": "108252007",
        "display": "Laboratory procedure",
    }
]
category = category_obj
code_obj = CodeableConcept()
code_obj.coding = [
    {
        "system": "http://snomed.info/sct",
        "code": "252150008",
        "display": "Fasting lipid profile",
    }
]
code_obj.text = "Fasting lipid profile"
code = CodeableReference()  # this CODE part need to be checked furhter
code.concept = code_obj
authored = "2020-07-09T15:32:26.605+05:30"
requestor = {"reference": "Practitioner/1", "display": "Dr. DEF"}
serviceReq.meta = meta
serviceReq.id = "1"
serviceReq.text = text
serviceReq.code = code
serviceReq.subject = subject
serviceReq.authoredOn = authored
serviceReq.requester = requestor
serviceReq.category = [category]
# Convert the Patient resource to JSON
procedure_json = serviceReq.json()

print(procedure_json)
