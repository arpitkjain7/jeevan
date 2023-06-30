from typing import List, Optional
from pydantic import BaseModel


class RegisterPatient(BaseModel):
    abha_number: str
    purpose: str
    hip_id: str


class FetchRegisterationMode(BaseModel):
    abha_number: str
    purpose: str = "KYC_AND_LINK"
    hip_id: str


class AuthInit(BaseModel):
    abha_number: str
    purpose: str = "KYC_AND_LINK"
    auth_mode: str
    hip_id: str


class VerifyOtp(BaseModel):
    txnId: str
    otp: str


class VerifyDemographic(BaseModel):
    txnId: str
    name: str
    gender: str
    dateOfBirth: str
    mobileNumber: str


class RegisterWithoutABHA(BaseModel):
    name: str
    gender: str
    DOB: str
    mobile_number: str
    hip_id: str


class UpdatePatient(BaseModel):
    pid: str
    name: str
    gender: str
    DOB: str
    mobile_number: str
    hip_id: str
