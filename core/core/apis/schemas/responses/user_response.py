from typing import List
from pydantic import BaseModel
import datetime


class RegisterResponse(BaseModel):
    access_token: str
    token_type: str
    user_role: str
    status: str


class LoginResponse(BaseModel):
    id: int
    username: str
    name: str
    hip_name: str
    hip_id: str
    user_role: str
    department: str
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    hip_name: str
    hip_id: str
    user_role: str
    department: str
