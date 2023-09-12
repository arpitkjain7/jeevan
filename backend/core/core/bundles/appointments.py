from fhir.resources.appointment import Appointment
from fhir.resources.appointment import AppointmentParticipant
from fhir.resources.servicerequest import ServiceRequest
from fhir.resources.meta import Meta
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from datetime import datetime
import json

appointment = Appointment(resource_type="Appointment", status="booked", participant=[])
coding_obj = Coding()
codeable_obj = CodeableConcept()
codeable_obj.coding = [
    {
        "system": "http://snomed.info/sct",
        "code": "408443003",
        "display": "General medical practice",
    }
]
appointment.serviceCategory = [codeable_obj]
meta = Meta(
    versionId=1,
    lastUpdated=datetime.now(),
    profile=["https://nrces.in/ndhm/fhir/r4/StructureDefinition/Appointment"],
)

appointment_json = appointment.json()
