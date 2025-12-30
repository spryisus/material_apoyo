from abc import ABC, abstractmethod
from typing import Protocol, Optional, List, Any
from sqlalchemy.orm import InstrumentedAttribute
from app.models.photo_model import Photo

class IPhotoRepository(Protocol):
    @abstractmethod
    def get(self, value: Any, column: InstrumentedAttribute) -> Optional[Photo]:
        pass

    @abstractmethod
    def get_all(self) -> List[Photo]:
        pass

    @abstractmethod
    def get_where(self, *conditions) -> List[Photo]:
        pass

    @abstractmethod
    def create(self, obj_in: Photo) -> Photo:
        pass

    @abstractmethod
    def update(self, db_obj: Photo, obj_in: dict) -> Photo:
        pass

    @abstractmethod
    def delete(self, value: Any, column: InstrumentedAttribute) -> bool:
        pass