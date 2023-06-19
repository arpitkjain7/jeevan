from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from core import Base


class MedicalHistory(Base):
    __tablename__ = "medicalHistory"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    pmr_id = Column(String, ForeignKey("patientMedicalRecord.id"))
    diabetes_melitus = Column(String)
    hypertension = Column(String)
    hypothyroidism = Column(String)
    alcohol = Column(String)
    tobacco = Column(String)
    smoke = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
