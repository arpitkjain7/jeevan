from typing import List, Optional
from pydantic import BaseModel
from datetime import date


class CreateHIP(BaseModel):
    name: str
    hip_id: str
    hip_address: str
    hip_contact_number: str
    hip_email_address: str
    hfr_reg_number: str
    hfr_status: str = "ACTIVE"
