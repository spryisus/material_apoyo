from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.db import Base

class UserDevice(Base):
    __tablename__ = "user_devices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    session_token = Column(String, unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
    fcm_token = Column(String, nullable=False)
    last_activity = Column(DateTime, server_default=func.now())
    device_type = Column(String)
    device_name = Column(String, nullable=True)
    device_os = Column(String, nullable=True)
    browser = Column(String, nullable=True) 
    ip_address = Column(String, nullable=True)
    last_login = Column(DateTime, server_default=func.now())
    last_logout = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
