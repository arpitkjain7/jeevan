from enum import unique
from sqlalchemy import Column, String, Integer, ForeignKey, JSON, DateTime, Float, VARCHAR
from core import Base


class ListOfDiagnosis(Base):
    __tablename__ = "listOfDiagnosis"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    disease = Column(String)
    disease_metadata = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
