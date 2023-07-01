from enum import unique
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    JSON,
    DateTime,
    TIME,
    Float,
    VARCHAR,
)
from core import Base


class DocDetails(Base):
    __tablename__ = "docDetails"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    doc_name = Column(String)
    hip_id = Column(String)
    doc_degree = Column(String)
    doc_specialization = Column(String)
    doc_department = Column(String)
    doc_working_days = Column(String)
    doc_reg_id = Column(String)
    avg_consultation_time = Column(String)
    consultation_start_time = Column(TIME)
    consultation_end_time = Column(TIME)
    consultation_fees = Column(Integer)
    follow_up_fees = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
