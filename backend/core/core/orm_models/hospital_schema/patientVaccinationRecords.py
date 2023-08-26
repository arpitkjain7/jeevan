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


class PatientVaccinationRecords(Base):
    __tablename__ = "patientVaccinationRecords"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String, ForeignKey("patientDetails.id"))
    vaccination_type = Column(String)
    vaccination_name = Column(String)
    vaccination_date = Column(DateTime)
    vaccination_metadata = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    __table_args__ = {"schema": "hospital_schema"}
