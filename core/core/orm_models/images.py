from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    Text,
    ARRAY,
    Boolean,
)
from sqlalchemy.ext.mutable import MutableList
from core import Base


class Images(Base):
    __tablename__ = "images"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(String, ForeignKey("users.email_id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    annotations = Column(ARRAY(String))
    s3_location = Column(String)
    s3_url = Column(Text)
    thumbnail_url = Column(Text)
    approved = Column(Boolean)
    valid_upto = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
