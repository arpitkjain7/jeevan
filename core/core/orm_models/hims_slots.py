from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Date, Time
from core import Base


class Slots(Base):
    __tablename__ = "slots"
    __table_args__ = {"extend_existing": True}
    slot_id = Column(Integer, primary_key=True, autoincrement=True)
    doc_id = Column(Integer, ForeignKey("docDetails.id"))
    patient_id = Column(String, ForeignKey("patientDetails.id"))
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    status = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
