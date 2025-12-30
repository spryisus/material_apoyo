from abc import ABC, abstractmethod
from typing import Protocol, Optional, List, Any
from sqlalchemy.orm import InstrumentedAttribute
from app.models.post_model import Post

class IPostRepository(Protocol):
    @abstractmethod
    def get(self, value: Any, column: InstrumentedAttribute) -> Optional[Post]:
        pass

    @abstractmethod
    def get_all(self) -> List[Post]:
        pass

    @abstractmethod
    def get_where(self, *conditions) -> List[Post]:
        pass

    @abstractmethod
    def create(self, obj_in: Post) -> Post:
        pass

    @abstractmethod
    def update(self, db_obj: Post, obj_in: dict) -> Post:
        pass

    @abstractmethod
    def delete(self, value: Any, column: InstrumentedAttribute) -> bool:
        pass