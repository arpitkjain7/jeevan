from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, JSON
from core import Base


class PatientMedicalRecord(Base):
    __tablename__ = "patientMedicalRecord"
    __table_args__ = {"extend_existing": True}
    id = Column(String, primary_key=True)
    hip_id = Column(String, ForeignKey("hipDetails.hip_id"))
    date_of_consultation = Column(DateTime)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    doc_id = Column(Integer, ForeignKey("docDetails.id"))
    patient_id = Column(String, ForeignKey("patientDetails.id"))
    advices = Column(String)
    notes = Column(String)
    raw_transcripts = Column(JSON)
    summarised_notes = Column(JSON)
    affiliated = Column(Boolean)
    abdm_linked = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
