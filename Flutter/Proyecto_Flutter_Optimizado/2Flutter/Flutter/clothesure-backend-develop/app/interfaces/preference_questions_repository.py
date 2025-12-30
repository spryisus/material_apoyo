from abc import ABC, abstractmethod
from typing import Protocol, Optional, List, Any
from sqlalchemy.orm import InstrumentedAttribute
from app.models.preference_questions_model import PreferenceQuestion

class IPreferenceQuestionRepository(Protocol):
    @abstractmethod
    def get(self, value: Any, column: InstrumentedAttribute) -> Optional[PreferenceQuestion]:
        pass

    @abstractmethod
    def get_all(self) -> List[PreferenceQuestion]:
        pass

    @abstractmethod
    def get_where(self, *conditions) -> List[PreferenceQuestion]:
        pass

    @abstractmethod
    def create(self, obj_in: PreferenceQuestion) -> PreferenceQuestion:
        pass

    @abstractmethod
    def update(self, db_obj: PreferenceQuestion, obj_in: dict) -> PreferenceQuestion:
        pass

    @abstractmethod
    def delete(self, value: Any, column: InstrumentedAttribute) -> bool:
        pass