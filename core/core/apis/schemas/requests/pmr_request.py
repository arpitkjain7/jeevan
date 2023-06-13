from typing import List, Optional
from pydantic import BaseModel
from datetime import date


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


class Complaint(BaseModel):
    complaint_type: str
    frequency: str
    severity: str
    duration: str


class Diagnosis(BaseModel):
    disease: str
    duration: str


class Medicines(BaseModel):
    medicine_name: str
    frequency: str
    time_of_day: str
    duration: str
    notes: str = None


class MedicalHistory(BaseModel):
    diabetes_melitus: str = None
    hypertension: str = None
    hypothyroidism: str = None
    alcohol: str = None
    tobacco: str = None
    smoke: str = None


class MedicalTests(BaseModel):
    name: str


class CreateVital(BaseModel):
    pmr_id: str
    data: List[Vital]


class UpdateVital(BaseModel):
    id: str
    pmr_id: str
    data: List[Vital]


class CreateComplaint(BaseModel):
    pmr_id: str
    data: List[Complaint]


class UpdateComplaint(BaseModel):
    id: str
    pmr_id: str
    data: List[Complaint]


class CreateDiagnosis(BaseModel):
    pmr_id: str
    data: List[Diagnosis]


class UpdateDiagnosis(BaseModel):
    id: str
    pmr_id: str
    data: List[Diagnosis]


class CreateMedication(BaseModel):
    pmr_id: str
    data: List[Medicines]


class UpdateMedication(BaseModel):
    id: str
    pmr_id: str
    data: List[Medicines]


class CreateMedicalTest(BaseModel):
    pmr_id: str
    data: List[MedicalTests]


class UpdateMedicalTest(BaseModel):
    id: str
    pmr_id: str
    data: List[MedicalTests]


class CreateMedicalHistory(BaseModel):
    pmr_id: str
    data: List[MedicalHistory]


class UpdateMedicalHistory(BaseModel):
    id: str
    pmr_id: str
    data: List[MedicalHistory]


class PMR(BaseModel):
    patient_id: str
    doc_id: int
    appointment_id: int
    hip_id: str
    date_of_consultation: date
    # vitals: List[Vital]
    # complaints: List[CreateComplaint]
    # diagnosis: List[CreateDiagnosis]
    # medication: List[CreateMedication]
    # medical_test: List[CreateMedicalTest]
    # medical_history: List[CreateMedicalHistory]
