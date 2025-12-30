from typing import TypeVar, Generic, Type, List, Optional, Any

from sqlalchemy import BinaryExpression
from sqlalchemy.orm import Session, InstrumentedAttribute
from sqlalchemy.exc import NoResultFound

ModelType = TypeVar("ModelType")

class BaseCRUD(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get(self, value: Any, column: InstrumentedAttribute) -> Optional[ModelType]:
        return self.db.query(self.model).filter(column == value).first()

    def get_where(self, *conditions: BinaryExpression) -> List[ModelType]:
        return self.db.query(self.model).filter(*conditions).all()

    def get_all(self) -> List[ModelType]:
        return self.db.query(self.model).all()

    def create(self, obj_in: ModelType) -> ModelType:
        self.db.add(obj_in)
        self.db.commit()
        self.db.refresh(obj_in)
        return obj_in

    def update(self, db_obj: ModelType, obj_in: dict) -> ModelType:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, value: Any, column: InstrumentedAttribute) -> bool:
        obj = self.get(value, column)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False


