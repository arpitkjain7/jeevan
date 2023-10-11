from typing import List, Optional
from pydantic import BaseModel
from datetime import time


class Template(BaseModel):
    name: str
    since: str = None
    severity: str = None
    notes: str = None
    snomed_code: str = None
    snomed_name: str = None


class TemplateDetails(BaseModel):
    template_name: str
    doc_id: str = None
    template_type: str = None
    values: List[Template]
