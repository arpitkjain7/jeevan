from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, Boolean
from core import Base


class PatientMedicalRecord(Base):
    __tablename__ = "patientMedicalRecord"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    hip_id = Column(String, ForeignKey("hipDetails.hip_id"))
    date_of_consultation = Column(DateTime)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    doc_id = Column(Integer, ForeignKey("docDetails.id"))
    height = Column(Float)
    weight = Column(Float)
    pulse = Column(Integer)
    blood_pressure = Column(String)
    body_temperature = Column(Float)
    patient_id = Column(String, ForeignKey("patientDetails.id"))
    abdm_linked = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
