from fhir.resources.appointment import Appointment, AppointmentParticipant
from fhir.resources.reference import Reference
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference

# Create a reference to the patient
patient_ref = Reference()
patient_ref.reference = "Patient/123"  # Replace with actual patient ID

# Create a reference to the practitioner
practitioner_ref = Reference()
practitioner_ref.reference = "Practitioner/456"  # Replace with actual practitioner ID

# Create a Coding instance for the SNOMED CT code
snomed_coding = Coding()
snomed_coding.system = "http://snomed.info/sct"
snomed_coding.code = "123456"  # Replace with actual SNOMED CT code
snomed_coding.display = "Appointment Reason Name"  # Replace with actual reason name

# Create a CodeableConcept instance for the reason
appointment_reason = CodeableConcept()
appointment_reason.coding = [snomed_coding]
refernce_obj = Reference(reference="Patient/1")
# Create an Appointment instance
appointment = Appointment(
    status="booked",
    participant=[
        AppointmentParticipant(actor=patient_ref, status="accepted"),
        AppointmentParticipant(actor=practitioner_ref, status="accepted"),
    ],
)
appointment.start = "2023-05-20T10:00:00Z"  # Replace with actual start time
appointment.end = "2023-05-20T10:30:00Z"  # Replace with actual end time

print(appointment.json())
