from typing import List, Optional
from pydantic import BaseModel
from datetime import time
from enum import Enum


class DocDetails(BaseModel):
    doc_name: str
    hip_id: str
    doc_degree: str
    affiliated: bool
    doc_working_days: str
    doc_specialization: str
    doc_department: str
    doc_working_days: str
    doc_licence_no: str
    avg_consultation_time: str
    consultation_start_time: time
    consultation_end_time: time
    consultation_fees: int
    follow_up_fees: int


class EducationDetails(BaseModel):
    college: str
    degree: str
    year: str


class UserRole(str, Enum):
    STAFF = "STAFF"
    DOCTOR = "DOCTOR"
    ADMIN = "ADMIN"


class DocDetailsV2(BaseModel):
    mobile_number: str
    password: str
    email_id: str
    doc_name: str
    hip_id: str
    user_role: str
    department: str
    doc_degree: str
    affiliated: bool
    doc_working_days: str
    doc_specialization: str
    doc_department: str
    doc_working_days: str
    doc_licence_no: str
    avg_consultation_time: str
    consultation_start_time: time
    consultation_end_time: time
    consultation_fees: int
    follow_up_fees: int
    years_of_experience: str
    commonly_treats: str
    bio: str
    education: List[EducationDetails]
    awards: str


class UpdateDoctor(BaseModel):
    doc_id: str
    data: List[DocDetails]


class ExternalDoc(BaseModel):
    doc_name: str
    doc_licence_no: str
