from enum import unique
from sqlalchemy import Column, String, Boolean, Integer, DateTime, TIME, JSON
from core import Base


class DocDetails(Base):
    __tablename__ = "docDetails"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    doc_uid = Column(String)  # This will be used as the path parameter.
    doc_name = Column(String)
    age = Column(String)
    languages = Column(String)
    email_id = Column(String)
    mobile_number = Column(String)
    bio = Column(String)
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
    years_of_experience = Column(String)
    commonly_treats = Column(String)
    google_reviews = Column(JSON)
    educational_content = Column(String)
    education = Column(JSON)
    external_hips = Column(JSON)
    awards = Column(String)
    profile_photo = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
