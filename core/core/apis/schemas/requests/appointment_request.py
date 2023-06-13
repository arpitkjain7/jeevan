from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class AppointmentType(str, Enum):
    AMB = "ambulatory"
    EMER = "emergency"
    FLD = "field"
    HH = "home health"
    IMP = "inpatient encounter"
    ACUTE = "inpatient acute"
    NONAC = "inpatient non-acute"
    OBSENC = "observation encounter"
    PRENC = "pre-admission"
    SS = "short stay"
    VR = "virtual"


class Create(BaseModel):
    doc_id: int
    patient_id: str
    appointment_type: AppointmentType
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
