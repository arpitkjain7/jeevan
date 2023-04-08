from typing import List, Optional
from pydantic import BaseModel, Field


class EventMetadata(BaseModel):
    event_date: str
    event_location: str = Field(None)
    event_bucket: str = Field(None)


class CreateEventResponse(BaseModel):
    event_id: int
    event_name: str
    owner_id: str
    event_metadata: EventMetadata


class Events(BaseModel):
    events: List[CreateEventResponse]
