from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from core import Base


class PatientDetails(Base):
    __tablename__ = "patientDetails"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    abha_number = Column(String)
    abha_address = Column(String)
    aadhar_number = Column(String)
    mobile_number = Column(String)
    name = Column(String)
    gender = Column(String)
    DOB = Column(String)
    address = Column(JSON)
    linking_token = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
