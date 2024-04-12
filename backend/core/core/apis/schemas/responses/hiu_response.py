from typing import List
from pydantic import BaseModel
from datetime import datetime


class Consent(BaseModel):
    id: str
    hip_id: str = None
    hip_name: str = None
    status: str
    hiu_id: str
    hiu_name: str = None
    purpose: str
    access_mode: str
    date_range: dict
    hi_type: dict = None
    expire_at: str
    abha_address: str
    created_at: datetime
    updated_at: datetime


class ConsentDetails(BaseModel):
    id: str
    hip_id: str = None
    hip_name: str = None
    status: str
    hiu_id: str
    hiu_name: str = None
    purpose: str
    access_mode: str
    date_range: dict
    hi_type: dict = None
    expire_at: str
    patient_data_transformed: list
