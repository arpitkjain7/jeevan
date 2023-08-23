from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from core import Base


class Token(Base):
    __tablename__ = "hims_token"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    token_number = Column(Integer)
    patient_id = Column(String, ForeignKey("patientDetails.id"))
    created_at = Column(DateTime)
