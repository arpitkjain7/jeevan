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
