from typing import List, Optional
from pydantic import BaseModel, Field


class FileUrl(BaseModel):
    file_url: str
    file_name: str


class AddImageUrl(BaseModel):
    files: str


class CreateEvent(BaseModel):
    event_name: str
    event_date: str
    event_location: str = Field(None)
