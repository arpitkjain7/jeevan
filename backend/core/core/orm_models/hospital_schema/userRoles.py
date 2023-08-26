from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, String
from core import Base
import enum


class RoleEnum(enum.Enum):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    STAFF = "STAFF"


class UserRoles(Base):
    __tablename__ = "userRoles"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_role = Column(Enum(RoleEnum))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    __table_args__ = {"schema": "hospital_schema"}
