from sqlalchemy import Column, String, Integer, DateTime, JSON
from core import Base


class GatewayInteraction(Base):
    __tablename__ = "gatewayInteraction"
    __table_args__ = {"extend_existing": True}
    request_id = Column(String, primary_key=True)
    request_type = Column(String)
    transaction_id = Column(String)
    request_status = Column(String)
    gateway_metadata = Column(JSON)
    token = Column(String)
    error_code = Column(String)
    error_message = Column(String)
    callback_response = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    __table_args__ = {"schema": "lobster_schema"}
