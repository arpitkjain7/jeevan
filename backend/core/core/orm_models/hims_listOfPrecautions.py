from enum import unique
from sqlalchemy import Column, String, Integer, ForeignKey, JSON, DateTime, Float, VARCHAR
from core import Base


class ListOfPrecautions(Base):
    __tablename__ = "listOfPrecautions"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    instructions = Column(String)
    medical_condition = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
