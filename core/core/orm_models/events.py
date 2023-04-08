from enum import unique
from sqlalchemy import Column, String, Integer, ForeignKey, JSON, DateTime
from core import Base


class Events(Base):
    __tablename__ = "events"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_uuid = Column(String)
    event_name = Column(String)
    owner_id = Column(String, ForeignKey("users.email_id"))
    event_pin = Column(String)
    event_status = Column(String, default="INACTIVE")
    event_metadata = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
