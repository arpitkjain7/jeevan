from enum import unique
from sqlalchemy import Column, String, Integer, ForeignKey, JSON, DateTime, Float, VARCHAR
from core import Base


class ListOfMedicines(Base):
    __tablename__ = "listOfMedicines"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    company = Column(String)
    medicine_metadata = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
