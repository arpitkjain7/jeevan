from enum import unique
from sqlalchemy import Column, String, Integer, ForeignKey, JSON, DateTime, Float, VARCHAR
from core import Base


class ListOfMedicalTests(Base):
    __tablename__ = "listOfMedicalTests"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    test_metadata = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
