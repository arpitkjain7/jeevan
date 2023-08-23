from sqlalchemy import Column, String, Integer, DateTime, UniqueConstraint
from core import Base


class Session(Base):
    __tablename__ = "session"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    hip_id = Column(String)
    parameter = Column(String)
    value = Column(String)
    type = Column(String)
    expires_in = Column(Integer)
    valid_till = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    __table_args__ = {UniqueConstraint("hip_id", "parameter", name="_hip_param_uc")}
