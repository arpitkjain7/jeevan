from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey
from core import Base


class HIUConsent(Base):
    __tablename__ = "hiu_consent"
    __table_args__ = {"extend_existing": True}
    id = Column(String, primary_key=True)
    status = Column(String)
    purpose = Column(String)
    patient = Column(String)
    hip_id = Column(String)
    hip_name = Column(String)
    hiu_id = Column(String)
    hiu_name = Column(String)
    hi_type = Column(JSON)
    access_mode = Column(String)
    date_range = Column(JSON)
    expire_at = Column(String)
    care_contexts = Column(JSON)
    requester_key_material = Column(JSON)
    patient_data_raw = Column(JSON)
    patient_data_transformed = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    __table_args__ = {"schema": "lobster_schema"}
