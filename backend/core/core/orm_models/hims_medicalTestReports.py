from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, JSON
from core import Base


class MedicalTestReports(Base):
    __tablename__ = "medicalTestReports"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    pmr_id = Column(String, ForeignKey("patientMedicalRecord.id"))
    medical_test_id = Column(Integer, ForeignKey("labInvestigations.id"))
    report_path = Column(String)
    report_metadata = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
