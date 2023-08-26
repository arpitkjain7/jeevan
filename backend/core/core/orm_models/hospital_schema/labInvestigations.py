from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from core import Base


class LabInvestigations(Base):
    __tablename__ = "labInvestigations"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    pmr_id = Column(String, ForeignKey("patientMedicalRecord.id"))
    snowmed_code = Column(String)
    snowmed_display = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    __table_args__ = {"schema": "hospital_schema"}
