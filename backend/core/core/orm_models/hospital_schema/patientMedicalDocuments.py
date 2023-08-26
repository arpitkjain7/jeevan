from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from core import Base


class PatientMedicalDocuments(Base):
    __tablename__ = "patientMedicalDocuments"
    __table_args__ = {"extend_existing": True}
    id = Column(String, primary_key=True)
    pmr_id = Column(String, ForeignKey("patientMedicalRecord.id"))
    document_name = Column(String)
    document_mime_type = Column(String)
    document_type = Column(String)
    document_type_code = Column(String)
    document_location = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    __table_args__ = {"schema": "hospital_schema"}
