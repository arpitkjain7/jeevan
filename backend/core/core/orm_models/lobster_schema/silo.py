from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from core import Base


class Silo(Base):
    __tablename__ = "silo"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    # pmr_id = Column(String, ForeignKey("patientMedicalRecord.id"))
    # condition = Column(String)
    # start_date = Column(DateTime)
    # status = Column(String)
    # notes = Column(String)
    # snowmed_code = Column(String)
    # snowmed_display = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    __table_args__ = {"schema": "abc_healthcare"}
