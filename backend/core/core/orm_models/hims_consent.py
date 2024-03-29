from sqlalchemy import Column, String, Integer, DateTime, JSON
from core import Base


class Consent(Base):
    __tablename__ = "consent"
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
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
