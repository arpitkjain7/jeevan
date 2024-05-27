from pydantic import BaseModel
from datetime import datetime


class PatientList(BaseModel):
    id: str
    patient_uid: str
    name: str
    abha_number: str
    mobile_number: str
    created_at: datetime
    updated_at: datetime
