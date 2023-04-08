from typing import List, Optional
from pydantic import BaseModel, Field


class Register(BaseModel):
    password: str
    email_id: str
    name: str = None
    phone_number: int = Field(None, description="User phone number")
    user_role: str = None


class Login(BaseModel):
    username: str = Field(..., description="User email")
    password: str = Field(..., description="Password")


class SSO(BaseModel):
    email_id: str = Field(None, description="User email Id")
    name: str = Field(None, description="Name of the user")


# class ForgotPassword(BaseModel):
#     username: str
#     new_password: str


# class UpdatePassword(BaseModel):
#     username: str
#     old_password: str
#     new_password: str
