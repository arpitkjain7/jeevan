from typing import List, Optional
from pydantic import BaseModel


class RegisterPatient(BaseModel):
    abha_number: str
    purpose: str
    hip_id: str


class FetchRegisterationMode(BaseModel):
    abha_number: str
    purpose: str
    hip_id: str
