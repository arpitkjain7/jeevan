from sqlalchemy import Column, Integer, ForeignKey, DateTime
from core import Base


class MedicalTest(Base):
    __tablename__ = "medicalTest"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    pmr_id = Column(Integer, ForeignKey("patientMedicalRecord.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
