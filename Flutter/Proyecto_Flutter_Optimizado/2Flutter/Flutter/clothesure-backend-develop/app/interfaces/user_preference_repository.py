from abc import ABC, abstractmethod
from typing import Protocol, Optional, List, Any
from sqlalchemy.orm import InstrumentedAttribute
from app.models.user_preference_model import UserPreference

class IUserPreferenceRepository(Protocol):
    @abstractmethod
    def get(self, value: Any, column: InstrumentedAttribute) -> Optional[UserPreference]:
        pass

    @abstractmethod
    def get_all(self) -> List[UserPreference]:
        pass

    @abstractmethod
    def get_where(self, *conditions) -> List[UserPreference]:
        pass

    @abstractmethod
    def create(self, obj_in: UserPreference) -> UserPreference:
        pass

    @abstractmethod
    def update(self, db_obj: UserPreference, obj_in: dict) -> UserPreference:
        pass

    @abstractmethod
    def delete(self, value: Any, column: InstrumentedAttribute) -> bool:
        pass