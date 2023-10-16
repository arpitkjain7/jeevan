from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Date, Time
from sqlalchemy.dialects.postgresql import JSONB
from core import Base


class Template(Base):
    __tablename__ = "templates"
    __table_args__ = {"extend_existing": True}
    template_id = Column(Integer, primary_key=True, autoincrement=True)
    doc_id = Column(Integer, ForeignKey("docDetails.id"))
    template_name = Column(String)
    template_type = Column(String)
    values = Column(JSONB)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
