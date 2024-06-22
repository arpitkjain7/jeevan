from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class Purpose(str, Enum):
    CAREMGT = "Care Management"
    BTG = "Break the Glass"
    PUBHLTH = "Public Health"
    HPAYMT = "Healthcare Payment"
    DSRCH = "Disease Specific Healthcare Research"
    PATRQT = "Self Requested"


class HiType(str, Enum):
    Prescription = "Prescription"
    DiagnosticReport = "Diagnostic Report"
    OPConsultation = "OP Consultation"
    DischargeSummary = "Discharge Summary"
    ImmunizationRecord = "Immunization Record"
    HealthDocumentRecord = "Record artifact"
    WellnessRecord = "Wellness Record"


class RaiseConsent(BaseModel):
    abha_address: str
    purpose: Purpose
    patient_id: str
    hi_type: list[HiType]
    date_from: str
    date_to: str
    expiry: str
    hip_id: str
    doc_id: str


class FindPatient(BaseModel):
    abha_address: str
    hiu_id: str
