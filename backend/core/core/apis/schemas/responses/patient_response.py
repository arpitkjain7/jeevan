from pydantic import BaseModel
from datetime import datetime


class PatientList(BaseModel):
    id: str
    patient_uid: str
    name: str
    abha_number: str = None
    mobile_number: str = None
    created_at: datetime
    updated_at: datetime
