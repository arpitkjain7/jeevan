from typing import List, Optional
from pydantic import BaseModel


class UpdateDoctor(BaseModel):
    doc_id: str
    name: str
    monday_availability = str
    tuesday_availability = str
    wednesday_availability = str
    thursday_availability = str
    friday_availability = str
    saturday_availability = str
    sunday_availability = str
    unavailability = str
    consultation_fees = int
    follow_up_fees = int
    hip_id: str
