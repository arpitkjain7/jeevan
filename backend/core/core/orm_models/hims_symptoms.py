from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from core import Base


class Symptoms(Base):
    __tablename__ = "symptoms"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    pmr_id = Column(String, ForeignKey("patientMedicalRecord.id"))
    symptom = Column(String)
    duration = Column(String)
    severity = Column(String)
    notes = Column(String)
    start_date = Column(DateTime)
    snowmed_code = Column(String)
    snowmed_display = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
