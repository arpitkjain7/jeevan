from typing import List, Optional
from pydantic import BaseModel, Field


class Register(BaseModel):
    password: str
    username: str
    name: str
    hip_name: str
    hip_id: str
    user_role: str
    department: str


class Login(BaseModel):
    email_id: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


# class ForgotPassword(BaseModel):
#     username: str
#     new_password: str


# class UpdatePassword(BaseModel):
#     username: str
#     old_password: str
#     new_password: str
