from fhir.resources.encounter import Encounter
from fhir.resources.identifier import Identifier
from fhir.resources.period import Period
from fhir.resources.meta import Meta
from fhir.resources.bundle import Bundle
from fhir.resources.coding import Coding
from fhir.resources.encounter import EncounterDiagnosis
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.codeablereference import CodeableReference
from fhir.resources.reference import Reference
from datetime import datetime
import json

# this code needs to be checked again
# something wrong with the diagnosis part
encounter = Encounter(resource_type="Encounter", status="finished")
meta = Meta(
    versionId=1,
    lastUpdated=datetime.now(),
    profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Encounter"],
)
bundle = Bundle(type="document")
text = {
    "status": "generated",
    "div": '<div xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-IN" lang="en-IN">Out Patient Consultation Encounter</div>',
}

identifier = Identifier()
identifier.system = "https://ndhm.in"
identifier.value = "S100"

cls = {
    "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
    "code": "AMB",
    "display": "ambulatory",
}

patient_ref = Reference()
patient_ref.reference = "Patient/123"
# subject = {
#     "reference": "Patient/1",
# }

period = Period(start="2020-07-09T14:58:58.181+05:30")

condition_ref = Reference()
condition_ref.reference = "Condition/1"

condition_1 = CodeableReference()
condition_1.reference = condition_ref

use_1 = CodeableConcept()
use_1.coding = [
    {
        "system": "http://snomed.info/sct",
        "code": "33962009",
        "display": "Chief complaint",
    }
]

diagnosis1 = EncounterDiagnosis()
diagnosis1.use = [use_1]
diagnosis1.condition = [condition_1]

# diagnosis = {
#     "condition": {"reference": "Condition/1"},
#     "use": {
#         "coding": [
#             {
#                 "system": "http://snomed.info/sct",
#                 "code": "33962009",
#                 "display": "Chief complaint",
#             }
#         ]
#     },
# }

encounter.meta = meta
encounter.text = text
encounter.identifier = [identifier]
# encounter.status = "finished"
encounter.subject = patient_ref
encounter.diagnosis = [diagnosis1]

# Convert the Patient resource to JSON
encounter_json = encounter.json()
