from enum import unique
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    JSON,
    DateTime,
    Float,
    VARCHAR,
)
from core import Base


class PatientMedicalRecord(Base):
    __tablename__ = "patientMedicalRecord"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_of_consultation = Column(DateTime)
    doc_id = Column(Integer, ForeignKey("docDetails.id"))
    height = Column(Float)
    weight = Column(Float)
    pulse = Column(Integer)
    blood_pressure = Column(String)
    body_temperature = Column(Float)
    patient_id = Column(Integer, ForeignKey("patientDetails.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
