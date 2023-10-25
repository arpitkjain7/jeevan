from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class VitalType(str, Enum):
    height = "HT"
    weight = "WT"
    pulse = "PLS"
    blood_pressure = "BP"
    body_temperature = "BT"
    oxygen_saturation = "OS"
    respiratory_rate = "RR"
    body_mass_index = "BMI"
    systolic_blood_pressure = "SBP"
    diastolic_blood_pressure = "DBP"


class Read(BaseModel):
    patient_id: str
    vital_type: VitalType
