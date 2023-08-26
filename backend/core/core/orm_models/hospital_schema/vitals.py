from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from core import Base


class Vital(Base):
    __tablename__ = "vitals"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    pmr_id = Column(String, ForeignKey("patientMedicalRecord.id"))
    height = Column(String)
    weight = Column(String)
    pulse = Column(String)
    blood_pressure = Column(String)
    body_temperature = Column(String)
    oxygen_saturation = Column(String)
    respiratory_rate = Column(String)
    body_mass_index = Column(String)
    systolic_blood_pressure = Column(String)
    diastolic_blood_pressure = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    __table_args__ = {"schema": "hospital_schema"}
