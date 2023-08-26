from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text, JSON
from core import Base


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    mobile_number = Column(String)
    hip_details = Column(JSON)
    department = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    __table_args__ = {"schema": "hospital_schema"}
