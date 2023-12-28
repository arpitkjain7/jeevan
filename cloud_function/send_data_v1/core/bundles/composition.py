from fhir.resources.composition import Composition, CompositionSection
from fhir.resources.humanname import HumanName
from fhir.resources.bundle import Bundle
from fhir.resources.meta import Meta
from fhir.resources.contactdetail import ContactDetail
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.identifier import Identifier
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.reference import Reference
from datetime import datetime
import json


def section(title, coding_system, coding_code, coding_display, reference):
    section = CompositionSection()
    code_obj = CodeableConcept()
    code_obj.coding = [
        {
            "system": coding_system,
            "code": coding_code,
            "display": coding_display,
        }
    ]
    ref = Reference()
    ref.reference = reference
    section.title = title
    section.code = code_obj
    section.entry = [ref]
    return section


codeable_obj = CodeableConcept()
codeable_obj.text = "Clinical Consultation report"
codeable_obj.coding = [
    {
        "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
        "code": "active",
        "display": "Active",
    }
]
author_ref = Reference()
author_ref.reference = "Practitioner/1"
author_ref.display = "Dr. DEF"


composition = Composition(
    resource_type="Composition",
    id="1",
    date="2020-07-09T15:32:26.605+05:30",
    title="Consultation Report",
    status="final",
    author=[author_ref],
    type=codeable_obj,
)
meta = Meta(
    versionId=1,
    lastUpdated="2015-02-07T13:28:17.239+02:00",
    profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord"],
)
bundle = Bundle(type="document")
text = {
    "status": "generated",
    "div": '<div xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-IN" lang="en-IN">\n      <p>No Known Allergy</p>\n      <p>recordedDate:2015-08-06</p>\n    </div>',
}
identifier = Identifier()
identifier.system = "https://ndhm.in"
identifier.value = "S100"

patient_ref = Reference()
patient_ref.reference = "Patient/123"
patient_ref.display = "Patient1"
encounter_ref = Reference()
encounter_ref.reference = "Encounter/123"
custodian_ref = Reference()
custodian_ref.reference = "Organization/1"
custodian_ref.display = "UVW Hospital"
section0 = section(
    "Chief complaints",
    "http://snomed.info/sct",
    "422843007",
    "Chief complaint section",
    "Condition/1",
)
section1 = section(
    "Chief complaints",
    "http://snomed.info/sct",
    "422843007",
    "Chief complaint section",
    "Condition/1",
)
section2 = section(
    "Chief complaints",
    "http://snomed.info/sct",
    "422843007",
    "Chief complaint section",
    "Condition/1",
)


composition.id = "1"
composition.meta = meta
composition.text = text
composition.identifier = [identifier]
composition.type = codeable_obj
composition.subject = [patient_ref]
composition.encounter = encounter_ref
# composition.date = date
# recorder is not working
# "recorder": {
#  "reference": "Practitioner/1"
# },
# allergyIntolerance.recorder
composition.custodian = custodian_ref
composition.section = [section0, section1, section2]


composition_json = composition.json()
