from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date
from enum import Enum


class AbhaRegistration(BaseModel):
    firstName: str
    middleName: str = None
    lastName: str
    email: str
    healthId: str
    password: str
    hip_id: str
    txnId: str


class OTPVerification(BaseModel):
    otp: str
    txnId: str


class OTPVerificationV3(BaseModel):
    otp: str
    mobileNumber: str
    txnId: str
    hipId: str


class abhaAddressCreation(BaseModel):
    abhaAddress: str
    txnId: str


class AbhaAuth(BaseModel):
    authMethod: str
    patientId: str = None
    abhaNumber: str = None


class AbhaAuthConfirm(BaseModel):
    otp: str
    txnId: str
    patientId: str = None
    authMode: str
    hidId: str


class MobileOTP(BaseModel):
    mobileNumber: str
    txnId: str


class AadhaarNumber(BaseModel):
    aadhaarNumber: str


class HealthNumber(BaseModel):
    healthNumber: str


class AbhaRegistration_MobileOTP(BaseModel):
    firstName: str
    lastName: str
    email: str
    healthId: str
    gender: str
    txnId: str
    hip_id: str
    dob: str


class MobileNumber(BaseModel):
    mobileNumber: str


class PatientData(BaseModel):
    patientId: str


class AbhaDetailsUpdateMode(str, Enum):
    mobile = "mobile"
    email = "email"
    aadhaar = "aadhaar"


class UpdateAbhaDetails(BaseModel):
    txnId: str
    mode: AbhaDetailsUpdateMode
    mobile: str = None
    email: str = None


class UpdateAbhaDetailsVerifyOTP(BaseModel):
    txnId: str
    mode: AbhaDetailsUpdateMode
    otp: str


class RetrieveAbhaMode(str, Enum):
    mobile = "mobile"
    aadhaar = "aadhaar"


class RetrieveAbhaGenerateOTP(BaseModel):
    mode: AbhaDetailsUpdateMode
    mobile: str = None
    aadhaar: str = None


class RetrieveAbhaVerifyOTP(BaseModel):
    txnId: str
    mode: AbhaDetailsUpdateMode
    otp: str


class RetrieveAbhaVerifyUser(BaseModel):
    txnId: str
    abhaNumber: str
    token: str
