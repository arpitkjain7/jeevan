from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from core import Base


class CurrentMedicines(Base):
    __tablename__ = "currentMedicines"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    pmr_id = Column(String, ForeignKey("patientMedicalRecord.id"))
    medicine_name = Column(String)
    start_date = Column(DateTime)
    status = Column(String)
    notes = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
