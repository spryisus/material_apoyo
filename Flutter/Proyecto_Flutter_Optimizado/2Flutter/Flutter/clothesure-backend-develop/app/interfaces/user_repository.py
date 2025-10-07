from abc import ABC, abstractmethod
from typing import Protocol, Optional, List, Any
from sqlalchemy.orm import InstrumentedAttribute
from app.models.user_model import User

class IUserRepository(Protocol):
    @abstractmethod
    def get(self, value: Any, column: InstrumentedAttribute) -> Optional[User]:
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def get_where(self, *conditions) -> List[User]:
        pass

    @abstractmethod
    def create(self, obj_in: User) -> User:
        pass

    @abstractmethod
    def update(self, db_obj: User, obj_in: dict) -> User:
        pass

    @abstractmethod
    def delete(self, value: Any, column: InstrumentedAttribute) -> bool:
        pass