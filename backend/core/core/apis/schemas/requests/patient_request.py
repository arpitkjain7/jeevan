from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class RegisterPatient(BaseModel):
    abha_number: str
    purpose: str
    hip_id: str


class FetchRegisterationMode(BaseModel):
    abha_number: str
    purpose: str = "KYC_AND_LINK"
    hip_id: str


class AuthMode(str, Enum):
    MOBILE_OTP = "MOBILE_OTP"
    AADHAAR_OTP = "AADHAAR_OTP"


class PatientAuth(BaseModel):
    abha_identifier: str
    mode: AuthMode


class PatientAuthResendOTP(BaseModel):
    mode: AuthMode
    txnId: str


class PatientAuthVerifyOTP(BaseModel):
    mode: AuthMode
    hip_id: str
    txnId: str
    otp: str


class AuthInit(BaseModel):
    abha_address: str
    purpose: str = "KYC_AND_LINK"
    auth_mode: str
    hip_id: str


class AuthInitV2(BaseModel):
    patient_id: str
    purpose: str = "KYC_AND_LINK"
    auth_mode: str


class VerifyOtp(BaseModel):
    txnId: str
    otp: str


class VerifyDemographic(BaseModel):
    txnId: str
    patient_id: str


class RegisterWithoutABHA(BaseModel):
    id: str = None
    name: str
    gender: str
    DOB: str
    mobile_number: str
    hip_id: str
    email: str = None


class UpdatePatient(BaseModel):
    pid: str
    name: str
    gender: str
    DOB: str
    mobile_number: str
    hip_id: str


class RegisterPatientV3(BaseModel):
    id: str = None
    abha_number: str = None
    abha_address: str = None
    primary_abha_address: str = None
    mobile_number: str = None
    name: str = None
    gender: str = None
    DOB: str = None
    age: str = None
    email: str = None
    address: str = None
    pincode: str = None
    hip_id: str = None
    auth_methods: str = None


class VerifyPatient(BaseModel):
    patient_id: str
