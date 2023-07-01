from typing import List, Optional
from pydantic import BaseModel
from datetime import time


class UpdateDoctor(BaseModel):
    doc_id: str
    doc_name: str
    doc_working_days: str
    avg_consultation_time: str
    start_time: time
    end_time: time
    consultation_fees: int
    follow_up_fees: int
    hip_id: str
