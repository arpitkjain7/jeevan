from typing import List, Optional
from pydantic import BaseModel
from datetime import date


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


class PMR(BaseModel):
    patient_id: str
    doc_id: int
    appointment_id: int
    height: float
    weight: float
    pulse: float
    blood_pressure: str
    body_temperature: float
    oxygen_saturation: float
    respiratory_rate: float
    body_mass_index: float
    systolic_blood_pressure: int
    diastolic_blood_pressure: int
    date_of_consultation: date
    hip_id: str


class CreateComplaint(BaseModel):
    pmr_id: str
    data: List[Complaint]


class CreateDiagnosis(BaseModel):
    pmr_id: str
    data: List[Diagnosis]


class CreateMedication(BaseModel):
    pmr_id: str
    data: List[Medicines]


class CreateMedicalTest(BaseModel):
    pmr_id: str
    data: List[MedicalTests]


class CreateMedicalHistory(BaseModel):
    pmr_id: str
    data: List[MedicalHistory]
