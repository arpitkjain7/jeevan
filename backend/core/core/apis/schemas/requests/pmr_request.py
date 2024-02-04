from typing import List, Optional
from pydantic import BaseModel
from datetime import date
from enum import Enum


class Vital(BaseModel):
    id: int = None
    height: str = None
    weight: str = None
    pulse: str = None
    body_temperature: str = None
    oxygen_saturation: str = None
    respiratory_rate: str = None
    body_mass_index: str = None
    systolic_blood_pressure: str = None
    diastolic_blood_pressure: str = None


class ExaminationFindings(BaseModel):
    id: int = None
    disease: str = None
    notes: str = None
    snowmed_code: str = None
    snowmed_display: str = None


class Diagnosis(BaseModel):
    id: int = None
    disease: str = None
    diagnosis_type: str = None
    status: str = None
    notes: str = None
    snowmed_code: str = None
    snowmed_display: str = None


class Symptoms(BaseModel):
    id: int = None
    symptom: str = None
    duration: str = None
    severity: str = None
    notes: str = None
    snowmed_code: str = None
    snowmed_display: str = None


class Medicines(BaseModel):
    id: int = None
    medicine_name: str = None
    frequency: str = None
    dosage: str = None
    time_of_day: str = None
    duration: str = None
    notes: str = None
    snowmed_code: str = None
    snowmed_display: str = None


# TODO: To be used in future
# class CurrentMedicines(BaseModel):
#     medicine_name: str = None
#     start_date: str = None
#     status: str = None
#     notes: str = None
#     snowmed_code: str = None
#     snowmed_display: str = None


class MedicalHistory(BaseModel):
    id: int = None
    medical_history: str = None
    since: str = None
    severity: str = None
    relationship: str = "self"
    notes: str = None
    snowmed_code: str = None
    snowmed_display: str = None


class LabInvestigations(BaseModel):
    id: int = None
    name: str = None
    notes: str = None
    snowmed_code: str = None
    snowmed_display: str = None


class CreateVital(BaseModel):
    pmr_id: str
    data: Vital


class UpdateVital(BaseModel):
    id: str
    pmr_id: str
    data: Vital


class CreateExaminationFindings(BaseModel):
    data: List[ExaminationFindings]


class CreateDiagnosis(BaseModel):
    data: List[Diagnosis]


class UpdateDiagnosis(BaseModel):
    id: str
    pmr_id: str
    data: List[Diagnosis]


class CreateSymptoms(BaseModel):
    data: List[Symptoms]


class UpdateSymptoms(BaseModel):
    id: str
    pmr_id: str
    data: List[Symptoms]


class CreateMedication(BaseModel):
    data: List[Medicines]


class UpdateMedication(BaseModel):
    id: str
    pmr_id: str
    data: List[Medicines]


# class CreateCurrentMedication(BaseModel):
#     data: List[CurrentMedicines]


# class UpdateCurrentMedication(BaseModel):
#     id: str
#     pmr_id: str
#     data: List[CurrentMedicines]


class CreateLabInvestigation(BaseModel):
    # pmr_id: str
    data: List[LabInvestigations]


class UpdateLabInvestigation(BaseModel):
    id: str
    pmr_id: str
    data: List[LabInvestigations]


class CreateMedicalHistory(BaseModel):
    # pmr_id: str
    data: List[MedicalHistory]


class UpdateMedicalHistory(BaseModel):
    id: str
    pmr_id: str
    data: List[MedicalHistory]


class Advice(BaseModel):
    advices: str = None


class Notes(BaseModel):
    notes: str = None


class CreatePMR(BaseModel):
    patient_id: str
    doc_id: int
    appointment_id: int
    hip_id: str


class ConsultationStatus(str, Enum):
    SCHED = "Scheduled"
    INP = "InProgress"
    PND = "Pending"
    COMP = "Completed"
    CANC = "Cancelled"


class CreatePMR_UpdateConsultation(BaseModel):
    patient_id: str
    doc_id: int
    appointment_id: int
    hip_id: str
    consultation_status: ConsultationStatus


# date_of_consultation: date
# vitals: List[Vital]
# complaints: List[CreateComplaint]
# diagnosis: List[CreateDiagnosis]
# medication: List[CreateMedication]
# medical_test: List[CreateMedicalTest]
# medical_history: List[CreateMedicalHistory]


class UpdateConsultationStatus(BaseModel):
    appointment_id: str
    consultation_status: ConsultationStatus


class FollowUp(BaseModel):
    appointment_id: str
    followup_date: date


class FollowUp_ConsultationStatus(BaseModel):
    appointment_id: str
    followup_date: date = None
    consultation_status: ConsultationStatus = None


class PMR(BaseModel):
    pmr_id: str
    vital: Vital = None
    examination_findings: CreateExaminationFindings = None
    diagnosis: CreateDiagnosis = None
    symptom: CreateSymptoms = None
    medication: CreateMedication = None
    lab_investigation: CreateLabInvestigation = None
    medical_history: CreateMedicalHistory = None
    advice: str = None
    notes: str = None


class DocumentTypes(str, Enum):
    DiagnosticReport = "Diagnostic Report"
    OPConsultation = "OP Consultation"
    DischargeSummary = "Discharge Summary"
    ImmunizationRecord = "Immunization Record"
    HealthDocumentRecord = "Record artifact"
    WellnessRecord = "Wellness Record"


class UploadDocument(BaseModel):
    pmr_id: str
    document_type: DocumentTypes


class NotificationChannel(str, Enum):
    WhatsApp = "whatsapp"
    SMS = "sms"


class SendNotification(BaseModel):
    pmr_id: str
    channel: NotificationChannel
    mobile_number: str = None


class PrescriptionMode(str, Enum):
    digital = "digital"
    handwritten = "handwritten"
