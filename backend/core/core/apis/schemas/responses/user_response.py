from typing import List
from pydantic import BaseModel
import datetime


class RegisterResponse(BaseModel):
    access_token: str
    token_type: str
    user_roles: list
    status: str


class LoginResponse(BaseModel):
    id: int
    username: str
    name: str
    hip_details: dict
    user_roles: list
    department: str
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    hip_details: dict
    user_roles: list
    department: str
