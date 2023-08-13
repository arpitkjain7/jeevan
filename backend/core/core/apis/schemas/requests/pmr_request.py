from typing import List, Optional
from pydantic import BaseModel
from datetime import date
from enum import Enum


class Vital(BaseModel):
    height: str
    weight: str
    pulse: str
    blood_pressure: str
    body_temperature: str
    oxygen_saturation: str
    respiratory_rate: str
    body_mass_index: str
    systolic_blood_pressure: str
    diastolic_blood_pressure: str


class ExaminationFindings(BaseModel):
    disease: str
    duration: str
    status: str
    snowmed_code: str
    snowmed_display: str


class Condition(BaseModel):
    condition: str
    start_date: str
    status: str
    notes: str = None
    snowmed_code: str
    snowmed_display: str


class Diagnosis(BaseModel):
    disease: str
    duration: str
    status: str
    notes: str = None
    snowmed_code: str
    snowmed_display: str


class Symptoms(BaseModel):
    symptom: str
    duration: str
    severity: str
    notes: str = None
    start_date: str
    snowmed_code: str
    snowmed_display: str


class Medicines(BaseModel):
    medicine_name: str
    frequency: str
    dosage: str
    time_of_day: str
    duration: str
    duration_period: str
    notes: str = None
    snowmed_code: str
    snowmed_display: str


class CurrentMedicines(BaseModel):
    medicine_name: str
    start_date: str
    status: str
    notes: str = None
    snowmed_code: str
    snowmed_display: str


class MedicalHistory(BaseModel):
    diabetes_melitus: str = None
    hypertension: str = None
    hypothyroidism: str = None
    alcohol: str = None
    tobacco: str = None
    smoke: str = None
    snowmed_code: str
    snowmed_display: str


class LabInvestigations(BaseModel):
    name: str
    snowmed_code: str
    snowmed_display: str


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
    vital: CreateVital
    condition: CreateCondition
    examinationFindings: CreateExaminationFindings
    diagnosis: CreateDiagnosis
    symptom: CreateSymptoms
    medication: CreateMedication
    currentMedication: CreateCurrentMedication
    lab_investigation: CreateLabInvestigation
    medical_history: CreateMedicalHistory


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


class Advice(BaseModel):
    pmr_id: str
    advices: str


class Notes(BaseModel):
    pmr_id: str
    notes: str
