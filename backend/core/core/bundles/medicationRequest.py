from fhir.resources.medicationrequest import MedicationRequest
from fhir.resources.identifier import Identifier
from fhir.resources.dosage import Dosage
from fhir.resources.bundle import Bundle
from fhir.resources.meta import Meta
from fhir.resources.codeablereference import CodeableReference
from fhir.resources.codeableconcept import CodeableConcept
from datetime import datetime
import json

subject = {"reference": "Patient/1", "display": "ABC"}
med_obj = CodeableConcept()
med_obj.coding = [
    {
        "system": "http://snomed.info/sct",
        "code": "252150008",
        "display": "Fasting lipid profile",
    }
]
med = CodeableReference()  # this CODE part need to be checked furhter
med.concept = med_obj
medicationReq = MedicationRequest(
    resource_type="MedicationRequest",
    subject=subject,
    status="active",
    intent="order",
    medication=med,
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
additional_obj = CodeableConcept()
additional_obj.coding = [
    {"system": "http://snomed.info/sct", "code": "229799001", "display": "Twice a day"}
]
route = CodeableConcept()
route.coding = [
    {
        "system": "http://snomed.info/sct",
        "code": "6064005",
        "display": "Topical route",
    }
]

dosage = Dosage()
dosage.additionalInstruction = [additional_obj]
dosage.route = route
authored = "2020-07-09"
requestor = {"reference": "Practitioner/1", "display": "Dr. DEF"}
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
