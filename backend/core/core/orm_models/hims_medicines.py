from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from core import Base


class Medicines(Base):
    __tablename__ = "medicines"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    pmr_id = Column(String, ForeignKey("patientMedicalRecord.id"))
    medicine_name = Column(String)
    dosage = Column(String)
    frequency = Column(String)
    time_of_day = Column(String)
    duration = Column(String)
    duration_period = Column(String)
    notes = Column(String)
    snowmed_code = Column(String)
    snowmed_display = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
