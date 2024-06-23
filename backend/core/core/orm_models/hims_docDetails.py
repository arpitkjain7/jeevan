from enum import unique
from sqlalchemy import Column, String, Boolean, Integer, DateTime, TIME, JSON
from core import Base


class DocDetails(Base):
    __tablename__ = "docDetails"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    doc_name = Column(String)
    hip_id = Column(String)
    doc_degree = Column(String)
    affiliated = Column(Boolean)
    doc_specialization = Column(String)
    doc_department = Column(String)
    doc_working_days = Column(String)
    doc_licence_no = Column(String)
    avg_consultation_time = Column(String)
    consultation_start_time = Column(TIME)
    consultation_end_time = Column(TIME)
    consultation_fees = Column(Integer)
    follow_up_fees = Column(Integer)
    experience = Column(String)
    commonly_treats = Column(String)
    about =  Column(String)
    address = Column(String)
    city = Column(String)
    location = Column(String)
    education = Column(JSON)
    awards = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
