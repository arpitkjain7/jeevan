from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from core import Base


class Complaint(Base):
    __tablename__ = "complaint"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    pmr_id = Column(String, ForeignKey("patientMedicalRecord.id"))
    complaint_type = Column(String)
    frequency = Column(String)
    severity = Column(String)
    duration = Column(String)
    start_date = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
