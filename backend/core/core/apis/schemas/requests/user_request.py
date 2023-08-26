from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class UserRoleEnum(str, Enum):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    STAFF = "STAFF"


class Register(BaseModel):
    password: str
    username: str
    mobile_number: str
    name: str
    hip_name: str
    hip_id: str
    department: str


class Login(BaseModel):
    email_id: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class LoginOTP(BaseModel):
    mobile_number: str


class VerifyOTP(BaseModel):
    mobile_number: str
    otp: int


class RoleAssignment(BaseModel):
    username: str
    role: list[UserRoleEnum]


# class ForgotPassword(BaseModel):
#     username: str
#     new_password: str


# class UpdatePassword(BaseModel):
#     username: str
#     old_password: str
#     new_password: str
