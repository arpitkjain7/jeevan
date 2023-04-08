from enum import unique
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from core import Base


class Appointments(Base):
    __tablename__ = "appointments"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_of_appointment = Column(DateTime)
    doc_id = Column(Integer, ForeignKey("docDetails.id"))
    patient_id = Column(Integer, ForeignKey("patientDetails.id"))
    notes = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
