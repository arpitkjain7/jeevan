from pydantic import BaseModel
from datetime import datetime


class PatientList(BaseModel):
    id: str
    patient_uid: str
    name: str
    abha_number: str = None
    mobile_number: str = None
    is_verified: bool
    gender: str
    age_in_years: str = None
    DOB: str = None
    email: str = None
    created_at: datetime
    updated_at: datetime
