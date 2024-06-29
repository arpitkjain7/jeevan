from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class EncounterType(str, Enum):
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


class AppointmentType(str, Enum):
    FIRST = "first visit"
    FOLLOWUP = "follow-up visit"


class Create(BaseModel):
    doc_id: int
    patient_id: str
    appointment_type: AppointmentType = None
    encounter_type: EncounterType = None
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

class BookAppointment(BaseModel):
    mobile_number: str = None
    name: str = None
    gender: str = None
    DOB: str = None
    age: str = None
    email: str = None
    address: str = None
    pincode: str = None
    hip_id: str = None
    doc_id: int
    appointment_start: str
    appointment_end: str = None