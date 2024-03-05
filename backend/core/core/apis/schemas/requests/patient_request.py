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
    pid: str


class RegisterWithoutABHA(BaseModel):
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
