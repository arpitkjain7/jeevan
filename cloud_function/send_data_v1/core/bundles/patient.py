from fhir.resources.patient import Patient
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

patient = Patient(resource_type="Patient")
meta = Meta(
    versionId=1,
    lastUpdated=datetime.now(),
    profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Patient"],
)
bundle = Bundle(type="document")
identifier = Identifier()
identifier.system = "https://healthid.ndhm.gov.in"
identifier.value = "53565645"
coding_obj = Coding()
codeable_obj = CodeableConcept()
codeable_obj.coding = [
    {
        "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
        "code": "MR",
        "display": "Medical record number",
    }
]
identifier.type = codeable_obj

patient.identifier = [identifier]
patient.meta = meta
# Set the patient's name
name = HumanName()
name.text = "Arpit Jain"
patient.name = [name]
contact_details = ContactDetail()
contact_point = ContactPoint()
contact_point = {"system": "phone", "value": "8923829323", "use": "home"}
patient.telecom = [contact_point]
patient.gender = "Male"
patient.birthDate = "1992-10-12"
# Convert the Patient resource to JSON
patient_json = patient.json()

print(patient_json)
