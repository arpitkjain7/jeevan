from sqlalchemy import Column, String, Integer, DateTime, JSON, Boolean
from core import Base


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    email_id = Column(String)
    mobile_number = Column(String)
    verified = Column(Boolean, default=False)
    otp = Column(Integer)
    hip_details = Column(JSON)
    user_role = Column(String)
    department = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
