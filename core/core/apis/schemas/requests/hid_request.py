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
