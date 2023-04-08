from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from core import Base


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)
    hip_name = Column(String)
    hip_id = Column(String)
    user_role = Column(String)
    department = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
