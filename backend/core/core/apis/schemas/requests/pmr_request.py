from typing import List, Optional
from pydantic import BaseModel
from datetime import date
from enum import Enum


class Vital(BaseModel):
    height: str = None
    weight: str = None
    pulse: str = None
    blood_pressure: str = None
    body_temperature: str = None
    oxygen_saturation: str = None
    respiratory_rate: str = None
    body_mass_index: str = None
    systolic_blood_pressure: str = None
    diastolic_blood_pressure: str = None


class ExaminationFindings(BaseModel):
    disease: str = None
    duration: str = None
    status: str = None
    snowmed_code: str = None
    snowmed_display: str = None


class Condition(BaseModel):
    condition: str = None
    start_date: str = None
    status: str = None
    notes: str = None
    snowmed_code: str = None
    snowmed_display: str = None


class Diagnosis(BaseModel):
    disease: str = None
    duration: str = None
    status: str = None
    notes: str = None
    snowmed_code: str = None
    snowmed_display: str = None


class Symptoms(BaseModel):
    symptom: str = None
    duration: str = None
    severity: str = None
    notes: str = None
    start_date: str = None
    snowmed_code: str = None
    snowmed_display: str = None


class Medicines(BaseModel):
    medicine_name: str = None
    frequency: str = None
    dosage: str = None
    time_of_day: str = None
    duration: str = None
    duration_period: str = None
    notes: str = None
    snowmed_code: str = None
    snowmed_display: str = None


class CurrentMedicines(BaseModel):
    medicine_name: str = None
    start_date: str = None
    status: str = None
    notes: str = None
    snowmed_code: str = None
    snowmed_display: str = None


class MedicalHistory(BaseModel):
    diabetes_melitus: str = None
    hypertension: str = None
    hypothyroidism: str = None
    alcohol: str = None
    tobacco: str = None
    smoke: str = None
    snowmed_code: str = None
    snowmed_display: str = None


class LabInvestigations(BaseModel):
    name: str = None
    snowmed_code: str = None
    snowmed_display: str = None


class CreateVital(BaseModel):
    pmr_id: str
    data: List[Vital]


class UpdateVital(BaseModel):
    id: str
    pmr_id: str
    data: List[Vital]


class CreateExaminationFindings(BaseModel):
    pmr_id: str
    data: List[ExaminationFindings]


class UpdateExaminationFindings(BaseModel):
    id: str
    pmr_id: str
    data: List[ExaminationFindings]


class CreateCondition(BaseModel):
    pmr_id: str
    data: List[Condition]


class UpdateCondition(BaseModel):
    id: str
    pmr_id: str
    data: List[Condition]


class CreateDiagnosis(BaseModel):
    pmr_id: str
    data: List[Diagnosis]


class UpdateDiagnosis(BaseModel):
    id: str
    pmr_id: str
    data: List[Diagnosis]


class CreateSymptoms(BaseModel):
    pmr_id: str
    data: List[Symptoms]


class UpdateSymptoms(BaseModel):
    id: str
    pmr_id: str
    data: List[Symptoms]


class CreateMedication(BaseModel):
    pmr_id: str
    data: List[Medicines]


class UpdateMedication(BaseModel):
    id: str
    pmr_id: str
    data: List[Medicines]


class CreateCurrentMedication(BaseModel):
    pmr_id: str
    data: List[CurrentMedicines]


class UpdateCurrentMedication(BaseModel):
    id: str
    pmr_id: str
    data: List[CurrentMedicines]


class CreateLabInvestigation(BaseModel):
    pmr_id: str
    data: List[LabInvestigations]


class UpdateLabInvestigation(BaseModel):
    id: str
    pmr_id: str
    data: List[LabInvestigations]


class CreateMedicalHistory(BaseModel):
    pmr_id: str
    data: List[MedicalHistory]


class UpdateMedicalHistory(BaseModel):
    id: str
    pmr_id: str
    data: List[MedicalHistory]


class CreatePMR(BaseModel):
    patient_id: str
    doc_id: int
    appointment_id: int
    hip_id: str


# date_of_consultation: date
# vitals: List[Vital]
# complaints: List[CreateComplaint]
# diagnosis: List[CreateDiagnosis]
# medication: List[CreateMedication]
# medical_test: List[CreateMedicalTest]
# medical_history: List[CreateMedicalHistory]


class PMR(BaseModel):
    pmr_id: str
    vital: CreateVital = None
    condition: CreateCondition = None
    examinationFindings: CreateExaminationFindings = None
    diagnosis: CreateDiagnosis = None
    symptom: CreateSymptoms = None
    medication: CreateMedication = None
    currentMedication: CreateCurrentMedication = None
    lab_investigation: CreateLabInvestigation = None
    medical_history: CreateMedicalHistory = None


class ConsultationStatus(str, Enum):
    SCHED = "scheduled"
    INP = "in progress"
    PND = "pending"
    COMP = "completed"
    CANC = "cancelled"


class UpdateConsultationStatus(BaseModel):
    appointment_id: str
    consultation_status: ConsultationStatus


class FollowUp(BaseModel):
    appointment_id: str
    followup_date: date


class DocumentTypes(str, Enum):
    Prescription = "Prescription"
    DiagnosticReport = "Diagnostic Report"
    OPConsultation = "OP Consultation"
    DischargeSummary = "Discharge Summary"
    ImmunizationRecord = "Immunization Record"
    HealthDocumentRecord = "Record artifact"
    WellnessRecord = "Wellness Record"


class UploadDocument(BaseModel):
    pmr_id: str
    document_type: DocumentTypes


class Advice(BaseModel):
    pmr_id: str
    advices: str


class Notes(BaseModel):
    pmr_id: str
    notes: str
