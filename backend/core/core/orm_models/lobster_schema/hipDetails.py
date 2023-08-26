from sqlalchemy import Column, String, Integer, DateTime
from core import Base


class HIPDetail(Base):
    __tablename__ = "hipDetails"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    hip_uid = Column(String)
    hip_id = Column(String, unique=True)
    hip_address = Column(String)
    hip_contact_number = Column(String)
    hip_email_address = Column(String)
    hfr_reg_number = Column(String)
    hfr_status = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    __table_args__ = {"schema": "lobster_schema"}
