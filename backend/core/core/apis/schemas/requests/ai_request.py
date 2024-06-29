from typing import List, Optional
from pydantic import BaseModel


class ConsultationSummary(BaseModel):
    comment: str
    summary: str


class Subjective(BaseModel):
    comment: str
    chief_complaint: str
    history_of_present_illness: List[str]
    past_medical_history: List[str]
    medication_history: List[str]
    allergy_information: List[str]
    family_history: List[str]
    social_history: List[str]
    review_of_systems: List[str]


class VitalSigns(BaseModel):
    blood_pressure: Optional[str]
    heart_rate: Optional[float]
    respiratory_rate: Optional[float]
    temperature: float
    oxygen_saturation: Optional[float]


class Objective(BaseModel):
    comment: str
    vital_signs: VitalSigns
    physical_examination_findings: Optional[str]
    laboratory_and_diagnostic_test_results: str


class Assessment(BaseModel):
    comment: str
    preliminary_diagnosis: str
    differential_diagnosis: Optional[str]
    risk_factors: Optional[str]


class Plan(BaseModel):
    diagnostic_plan: Optional[str]
    treatment_plan: str
    patient_education: Optional[str]
    follow_up: str


class TestsToBeTaken(BaseModel):
    comment: str
    laboratory_tests: List[str]
    imaging_tests: List[str]
    special_exams: List[str]


class OtherNextSteps(BaseModel):
    comment: str
    consultations: List[str]
    referrals: List[str]
    precautions: List[str]
    lifestyle_modifications: List[str]


class Medication(BaseModel):
    med_name: str
    instructions: Optional[str]
    dosages: Optional[str]
    duration_refill: Optional[str]


class Prescription(BaseModel):
    comment: str
    medications: List[Medication]


class AdditionalNotes(BaseModel):
    content: Optional[str]


class MedicalSummary(BaseModel):
    pmr_id: str
    consultation_summary: ConsultationSummary
    subjective: Subjective
    objective: Objective
    assessment: Assessment
    plan: Plan
    tests_to_be_taken: TestsToBeTaken
    other_next_steps: OtherNextSteps
    prescription: Prescription
    additional_notes: AdditionalNotes
