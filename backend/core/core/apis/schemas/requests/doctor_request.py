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


class Review(BaseModel):
    content: str
    name: str
    review_date: str
    rating: str


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
    about: str
    education: List[EducationDetails]
    awards: str
    external_hips: List[ExternalHIPDetails] = None
    languages: str = None
    google_reviews: List[Review] = None
    educational_content: str = None


class UpdateDoctor(BaseModel):
    id: str
    mobile_number: str = None
    email_id: str = None
    doc_first_name: str = None
    doc_last_name: str = None
    doc_uid: str = None
    hip_id: str = None
    age: str = None
    doc_degree: str = None
    affiliated: bool = None
    doc_specialization: str = None
    doc_department: str = None
    doc_working_days: str = None
    doc_licence_no: str = None
    avg_consultation_time: str = None
    consultation_start_time: time = None
    consultation_end_time: time = None
    consultation_fees: int = None
    follow_up_fees: int = None
    years_of_experience: str = None
    commonly_treats: str = None
    bio: str = None
    about: str = None
    education: List[EducationDetails] = None
    awards: str = None
    external_hips: List[ExternalHIPDetails] = None
    languages: str = None
    google_reviews: List[Review] = None
    educational_content: str = None


class ExternalDoc(BaseModel):
    doc_name: str
    doc_licence_no: str
