from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserDeviceBase(BaseModel):
    user_id: int
    fcm_token: Optional[str] = None
    device_type: Optional[str] = None
    device_name: Optional[str] = None
    device_os: Optional[str] = None
    browser: Optional[str] = None
    ip_address: Optional[str] = None
    session_token: Optional[str] = None
    is_active: Optional[bool] = True
    last_activity: Optional[datetime] = None


class UserDeviceCreate(UserDeviceBase):
    pass


class UserDeviceUpdate(BaseModel):
    fcm_token: Optional[str] = None
    device_type: Optional[str] = None
    device_name: Optional[str] = None
    device_os: Optional[str] = None
    browser: Optional[str] = None
    ip_address: Optional[str] = None
    session_token: Optional[str] = None
    is_active: Optional[bool] = None
    updated_by: Optional[int] = None


class UserDeviceOut(UserDeviceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: int
    updated_by: int
    last_login: Optional[datetime] = None
    last_logout: Optional[datetime] = None

    class Config:
        orm_mode = True
