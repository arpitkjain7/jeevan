from sqlalchemy import Column, String, Integer, DateTime
from core import Base


class Session(Base):
    __tablename__ = "session"
    __table_args__ = {"extend_existing": True}
    parameter = Column(String, primary_key=True)
    value = Column(String)
    type = Column(String)
    expires_in = Column(Integer)
    valid_till = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
