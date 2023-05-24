from fhir.resources.practitioner import Practitioner
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

practitioner = Practitioner(resource_type="Practitioner")
meta = Meta(
    versionId=1,
    lastUpdated=datetime.now(),
    profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Patient"],
)
#bundle = Bundle(type="document")
identifier = Identifier()
identifier.system = "https://doctor.ndhm.gov.in"
identifier.value = "21-1521-3828-3227"
coding_obj = Coding()
codeable_obj = CodeableConcept()
codeable_obj.coding = [
{
  "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
  "code": "MD",
  "display": "Medical License number"
}
]
identifier.type = codeable_obj

practitioner.identifier = [identifier]
practitioner.meta = meta
# Set the patient's name
name = HumanName()
name.text = "Dr. ABC"
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
