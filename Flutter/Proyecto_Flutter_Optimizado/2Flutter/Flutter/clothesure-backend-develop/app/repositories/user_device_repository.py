from app.core.basecrud import BaseCRUD
from app.models.user_device_model import UserDevice
from app.interfaces.user_device_repository import IUserDeviceRepository

class UserDeviceModel(BaseCRUD[UserDevice], IUserDeviceRepository):
    def __init__(self, db):
        super().__init__(UserDevice, db) 