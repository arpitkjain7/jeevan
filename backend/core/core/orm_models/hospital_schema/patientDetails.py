from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from core import Base


class PatientDetails(Base):
    __tablename__ = "patientDetails"
    __table_args__ = {"extend_existing": True}
    id = Column(String, primary_key=True)
    abha_number = Column(String)
    abha_address = Column(String)
    aadhar_number = Column(String)
    mobile_number = Column(String)
    name = Column(String)
    gender = Column(String)
    DOB = Column(String)
    email = Column(String)
    address = Column(String)
    village = Column(String)
    village_code = Column(String)
    town = Column(String)
    town_code = Column(String)
    district = Column(String)
    district_code = Column(String)
    pincode = Column(String)
    state_name = Column(String)
    state_code = Column(String)
    auth_methods = Column(JSON)
    hip_id = Column(String)
    abha_s3_location = Column(String)
    linking_token = Column(JSON)
    refresh_token = Column(JSON)
    access_token = Column(JSON)
    abha_status = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    __table_args__ = {"schema": "hospital_schema"}
