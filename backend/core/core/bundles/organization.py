from fhir.resources.organization import Organization
from fhir.resources.identifier import Identifier
from fhir.resources.bundle import Bundle
from fhir.resources.meta import Meta
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from datetime import datetime
import json

organization = Organization(resource_type="Organization")
meta = Meta(
    profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Organization"],
)
bundle = Bundle(type="document")
identifier = Identifier()
identifier.system = "https://facility.ndhm.gov.in"
identifier.value = "4567823"
coding_obj = Coding()
codeable_obj = CodeableConcept()
codeable_obj.coding = [
    {
        "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
        "code": "PRN",
        "display": "Provider number",
    }
]
identifier.type = codeable_obj

organization.identifier = [identifier]
organization.meta = meta
# Set the patient's name
name = "UVW Hospital"
organization.name = name
contact_point_1 = ContactPoint()
contact_point_1 = {
  "system": "phone",
  "value": "+91 273 2139 3632",
  "use": "work"
}
contact_point_2 = ContactPoint()
contact_point_2 = {
  "system": "email",
  "value": "contact@facility.uvw.org",
  "use": "work"
}
#telecom needs to be added
#organization.telecom = [contact_point_1,contact_point_2]
# Convert the Patient resource to JSON
organization_json = organization.json()

print(organization_json)
