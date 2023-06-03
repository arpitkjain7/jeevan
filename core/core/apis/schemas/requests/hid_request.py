from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date


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
