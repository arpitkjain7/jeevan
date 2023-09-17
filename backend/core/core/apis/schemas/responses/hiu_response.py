from typing import List
from pydantic import BaseModel
import datetime


class Consent(BaseModel):
    id: str
    hip_id: str
    hip_name: str
    status: str
    hiu_id: str
    hiu_name: str
    purpose: str
    access_mode: str
    date_range: dict
    hi_type: dict
    expire_at: str


class ConsentDetails(BaseModel):
    id: str
    hip_id: str
    hip_name: str
    status: str
    hiu_id: str
    hiu_name: str
    purpose: str
    access_mode: str
    date_range: dict
    hi_type: dict
    expire_at: str
    patient_data_transformed: list
