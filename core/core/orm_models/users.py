from enum import unique
from sqlalchemy import Column, String, Integer, DateTime, Numeric, ForeignKey
from core import Base


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)
    email_id = Column(String, unique=True)
    base_image_location = Column(String)
    phone_number = Column(Numeric)
    user_role = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
