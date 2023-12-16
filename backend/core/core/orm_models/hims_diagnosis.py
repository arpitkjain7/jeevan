from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from core import Base


class Diagnosis(Base):
    __tablename__ = "diagnosis"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    pmr_id = Column(String, ForeignKey("patientMedicalRecord.id"))
    disease = Column(String)
    diagnosis_type = Column(String)
    status = Column(String)
    notes = Column(String)
    start_date = Column(DateTime)
    snowmed_code = Column(String)
    snowmed_display = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
