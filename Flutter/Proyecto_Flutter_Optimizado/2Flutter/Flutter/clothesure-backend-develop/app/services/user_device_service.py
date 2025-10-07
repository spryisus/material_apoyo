from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.base_service import BaseService
from app.models.user_device_model import UserDevice
from app.repositories.user_device_repository import UserDeviceModel
from datetime import datetime, timedelta
import uuid

class UserDeviceService(BaseService):
    def __init__(self, repository: UserDeviceModel): 
        super().__init__(repository, UserDevice)

    def register_device_token(self, db: Session , user_id: int, token: str, device_type: str = None) -> None:
        existing = db.query(UserDevice).filter_by(
            user_id=user_id, fcm_token=token
        ).first()

        if not existing:
            new_device = UserDevice(
                user_id=user_id,
                fcm_token=token,
                device_type=device_type,
                created_by=user_id,
                updated_by=user_id
            )
            db.add(new_device)
            db.commit()

    def register_or_update_device(self, db: Session,user_id: int,fcm_token: str = None,device_type: str = None,device_name: str = None,device_os: str = None,browser: str = None,ip_address: str = None) -> UserDevice:

        device = db.query(UserDevice).filter(
            UserDevice.user_id == user_id,
            UserDevice.fcm_token == fcm_token
        ).first()

        if device:
            device.last_login = datetime.utcnow()
            device.is_active = True
            device.ip_address = ip_address
            device.device_type = device_type
            device.device_name = device_name
            device.device_os = device_os
            device.browser = browser
            device.last_activity = datetime.utcnow()
            db.commit()
            db.refresh(device)
        else:
            device = UserDevice(
                user_id=user_id,
                fcm_token=fcm_token,
                device_type=device_type,
                device_name=device_name,
                device_os=device_os,
                browser=browser,
                ip_address=ip_address,
                session_token=str(uuid.uuid4()),
                is_active=True,
                last_login=datetime.utcnow(),
                created_by=user_id,
                updated_by=user_id
            )
            db.add(device)
            db.commit()
            db.refresh(device)

        return device

    def logout_device(self, db: Session, session_token: str):
        device = db.query(UserDevice).filter_by(session_token=session_token).first()
        if device:
            device.is_active = False
            device.last_logout = datetime.utcnow()
            db.commit()
        return device

    def logout_all_devices(self,db: Session, user_id: int):
        db.query(UserDevice).filter_by(user_id=user_id, is_active=True).update(
            {"is_active": False, "last_logout": datetime.utcnow()}
        )
        db.commit()

    def mark_inactive_expired(self, db: Session, timeout_minutes: int = 5):
        threshold = datetime.utcnow() - timedelta(minutes=timeout_minutes)
        db.query(UserDevice).filter(
            UserDevice.is_active == True,
            UserDevice.last_activity < threshold
        ).update({"is_active": False})
        db.commit()

