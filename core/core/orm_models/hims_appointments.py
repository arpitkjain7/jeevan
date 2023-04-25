from enum import unique
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Date, Time
from core import Base


class Appointments(Base):
    __tablename__ = "appointments"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_date = Column(Date)
    appointment_time = Column(Time)
    hip_id = Column(String, ForeignKey("hipDetails.hip_id"))
    doc_id = Column(Integer, ForeignKey("docDetails.id"))
    patient_id = Column(String, ForeignKey("patientDetails.id"))
    token_number = Column(Integer)
    notes = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
