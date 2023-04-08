from enum import unique
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from core import Base


class Annotations(Base):
    __tablename__ = "annotations"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(Integer, ForeignKey("images.id"))
    user_id = Column(String, ForeignKey("users.email_id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    annotation_metadata = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
