from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from core import Base


class MedicalHistory(Base):
    __tablename__ = "medicalHistory"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    pmr_id = Column(String, ForeignKey("patientMedicalRecord.id"))
    medical_history = Column(String)
    relationship = Column(String)
    since = Column(String)
    severity = Column(String)
    notes = Column(String)
    snowmed_code = Column(String)
    snowmed_display = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
