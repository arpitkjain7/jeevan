from enum import unique
from sqlalchemy import Column, String, Integer, ForeignKey, JSON, DateTime
from core import Base


class Attendees(Base):
    __tablename__ = "attendees"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.email_id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    status = Column(String, default="INACTIVE")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
