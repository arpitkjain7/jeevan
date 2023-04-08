from typing import List
from pydantic import BaseModel
import datetime


class RegisterResponse(BaseModel):
    access_token: str
    token_type: str
    user_role: str


class LoginResponse(BaseModel):
    email: str
    name: str
    user_id: str
    access_token: str
    token_type: str
    user_role: str


class UpdateUserResponse(BaseModel):
    user_name: str
    license_type: str
    user_role: str
    user_role_id: str


class UserDetails(BaseModel):
    id: int
    name: str
    email_id: str
    password: str
    company_name: str
    sub_category_code: int
    location: str
    phone_number: int
    sub_category_name: str
    industry_name: str
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None
