from abc import ABC, abstractmethod
from typing import Protocol, Optional, List, Any
from sqlalchemy.orm import InstrumentedAttribute
from app.models.user_device_model import UserDevice

class IUserDeviceRepository(Protocol):
    @abstractmethod
    def get(self, value: Any, column: InstrumentedAttribute) -> Optional[UserDevice]:
        pass

    @abstractmethod
    def get_all(self) -> List[UserDevice]:
        pass

    @abstractmethod
    def get_where(self, *conditions) -> List[UserDevice]:
        pass

    @abstractmethod
    def create(self, obj_in: UserDevice) -> UserDevice:
        pass

    @abstractmethod
    def update(self, db_obj: UserDevice, obj_in: dict) -> UserDevice:
        pass

    @abstractmethod
    def delete(self, value: Any, column: InstrumentedAttribute) -> bool:
        pass