from typing import List, Optional
from pydantic import BaseModel, Field


class Register(BaseModel):
    mobile_number: str
    password: str
    name: str
    email_id: str = None


class OnBoard(BaseModel):
    mobile_number: str
    hip_name: str
    hip_id: str
    user_role: str
    department: str


class Login(BaseModel):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class ResetPassword(BaseModel):
    mobile_number: str
    old_password: str = None
    new_password: str
    otp: int = None


class GenerateOTP(BaseModel):
    mobile_number: str


class VerifyOTP(BaseModel):
    mobile_number: str
    otp: int


class ForgotPassword(BaseModel):
    mobile_number: str
    otp: int
    new_password: str


# class UpdatePassword(BaseModel):
#     username: str
#     old_password: str
#     new_password: str
