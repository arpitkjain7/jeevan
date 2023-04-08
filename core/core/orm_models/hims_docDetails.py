from enum import unique
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    JSON,
    DateTime,
    Float,
    VARCHAR,
)
from core import Base


class DocDetails(Base):
    __tablename__ = "docDetails"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    doc_name = Column(String)
    doc_degree = Column(String)
    doc_specialization = Column(String)
    doc_department = Column(String)
    doc_working_days = Column(String)
    doc_reg_id = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
