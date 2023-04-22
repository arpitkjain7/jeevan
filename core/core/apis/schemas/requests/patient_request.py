from typing import List, Optional
from pydantic import BaseModel


class RegisterPatient(BaseModel):
    abha_number: str
    purpose: str
    hip_id: str


class FetchRegisterationMode(BaseModel):
    abha_number: str
    purpose: str = "KYC_AND_LINK"


class AuthInit(BaseModel):
    abha_number: str
    purpose: str = "KYC_AND_LINK"
    auth_mode: str


class VerifyOtp(BaseModel):
    txnId: str
    otp: str


class VerifyDemographic(BaseModel):
    txnId: str
    name: str
    gender: str
    dateOfBirth: str
    mobileNumber: str
