from fhir.resources.medicationstatement import MedicationStatement
from fhir.resources.identifier import Identifier
from fhir.resources.reference import Reference
from fhir.resources.bundle import Bundle
from fhir.resources.meta import Meta
from fhir.resources.codeablereference import CodeableReference
from fhir.resources.codeableconcept import CodeableConcept
from datetime import datetime
import json

subject = {"reference": "Patient/1"}
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
medicationStatement = MedicationStatement(
    resource_type="MedicationStatement",
    subject=subject,
    status="completed",
    medication=med,
)
meta = Meta(
    profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/MedicationStatement"],
)
bundle = Bundle(type="document")
text = {
    "status": "generated",
    "div": '<div xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-IN" lang="en-IN">Atenolol 500 microgram/mL solution for injection</div>',
}
authored = "2020-07-09T15:32:26.605+05:30"
requestor = {"reference": "Practitioner/1", "display": "Dr. DEF"}
medicationStatement.meta = meta
medicationStatement.id = "1"
medicationStatement.text = text
medicationStatement.subject = subject
medicationStatement.dateAsserted = "2020-02-02T14:58:58.181+05:30"
# Convert the Patient resource to JSON
procedure_json = medicationStatement.json()

print(procedure_json)
