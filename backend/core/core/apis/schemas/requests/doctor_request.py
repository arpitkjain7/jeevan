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


class ExternalHIPDetails(BaseModel):
    name: str = None
    mobile_number: str = None
    location: str = None
    address: str = None
    doc_working_days: str = None
    consultation_start_time: str = None
    consultation_end_time: str = None


class UserRole(str, Enum):
    STAFF = "STAFF"
    DOCTOR = "DOCTOR"
    ADMIN = "ADMIN"


class DocDetailsV2(BaseModel):
    mobile_number: str
    password: str
    email_id: str
    doc_first_name: str
    doc_last_name: str
    doc_uid: str
    hip_id: str
    user_role: str
    age: str
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
    external_hips: List[ExternalHIPDetails] = None
    languages: str = None
    google_reviews: str = None
    educational_content: str = None


class UpdateDoctor(BaseModel):
    doc_id: str
    data: List[DocDetails]


class ExternalDoc(BaseModel):
    doc_name: str
    doc_licence_no: str
