from abc import ABC, abstractmethod
from typing import Protocol, Optional, List, Any
from sqlalchemy.orm import InstrumentedAttribute
from app.models.preference_options_model import PreferenceOption

class IPreferenceOptionRepository(Protocol):
    @abstractmethod
    def get(self, value: Any, column: InstrumentedAttribute) -> Optional[PreferenceOption]:
        pass

    @abstractmethod
    def get_all(self) -> List[PreferenceOption]:
        pass

    @abstractmethod
    def get_where(self, *conditions) -> List[PreferenceOption]:
        pass

    @abstractmethod
    def create(self, obj_in: PreferenceOption) -> PreferenceOption:
        pass

    @abstractmethod
    def update(self, db_obj: PreferenceOption, obj_in: dict) -> PreferenceOption:
        pass

    @abstractmethod
    def delete(self, value: Any, column: InstrumentedAttribute) -> bool:
        pass