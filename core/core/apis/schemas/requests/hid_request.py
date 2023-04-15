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
    txnId: str


class OTPVerification(BaseModel):
    otp: str = Field(..., description="OTP received")
    txn_id: str = Field(..., description="Txn Id")


class MobileOTP(BaseModel):
    mobile_number: str = Field(..., description="User Mobile Number")
    txn_id: str = Field(..., description="Txn Id")


class AadhaarNumber(BaseModel):
    aadhaar_number: str = Field(..., description="User Aadhaar Number")


class HealthNumber(BaseModel):
    health_number: str = Field(..., description="User Abha Address")
