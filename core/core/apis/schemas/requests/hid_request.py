from typing import List, Optional
from pydantic import BaseModel
from datetime import date


class AbhaRegistration(BaseModel):
    firstName: str
    middleName: str = None
    lastName: str
    email: str
    healthId: str
    password: str
    txnId: str


class OTPVerification(BaseModel):
    otp: str
    txn_id: str


class MobileOTP(BaseModel):
    mobile_number: str
    txn_id: str


class AadhaarNumber(BaseModel):
    aadhaar_number: str


class HealthNumber(BaseModel):
    health_number: str
