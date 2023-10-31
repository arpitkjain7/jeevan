from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class OnSubscribe(BaseModel):
    subscriber_id: str
    challenge: str
