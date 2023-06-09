from typing import List, Optional
from pydantic import BaseModel, Field


class Create(BaseModel):
    doc_id: int
    patient_id: str
    appointment_type: str
    hip_id: str
    appointment_start: str
    appointment_end: str = None


class Update(BaseModel):
    slot_id: int
    appointment_start: str
    appointment_end: str = None


class Read(BaseModel):
    doc_id: int
    date: str
