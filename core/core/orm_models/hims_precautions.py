from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from core import Base


class Precautions(Base):
    __tablename__ = "precautions"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    pmr_id = Column(String, ForeignKey("patientMedicalRecord.id"))
    notes = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
