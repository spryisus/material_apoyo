from typing import Any, Dict, Optional
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression
from fastapi import HTTPException
from app.services.audit_service import set_audit_fields  


class BaseService:
    def __init__(self, repo, model_class):
        self.repo = repo
        self.model_class = model_class
        
    def create(self, data: Dict, user_id: Optional[int] = None):
        obj = self.model_class(**data)
        set_audit_fields(obj, user_id, is_create=True)
        return self.repo.create(obj)
    
    def get(self, value: Any, column: InstrumentedAttribute):
        return self.repo.get(value, column)

    def get_where(self, *conditions: BinaryExpression):
        return self.repo.get_where(*conditions)

    def list_all(self):
        return self.repo.get_all()

    def update(self, value: Any, column: InstrumentedAttribute, data: Dict, user_id: Optional[int] = None):
        obj = self.repo.get(value, column)
        if not obj:
            return None
        set_audit_fields(obj, user_id, is_create=False)
        return self.repo.update(obj, data)
    
    def delete(self, value: Any, column: InstrumentedAttribute):
        return self.repo.delete(value, column)
    
    def get_or_none(self, value: Any, column: InstrumentedAttribute):
        """Devuelve el registro o None si no existe (similar a get)."""
        return self.repo.get(value, column)

    def get_or_404(self, value: Any, column: InstrumentedAttribute, error_msg: str = "Registro no encontrado"):
        """Devuelve el registro o lanza HTTP 404 si no existe."""
        record = self.repo.get(value, column)
        if not record:
            raise HTTPException(status_code=404, detail=error_msg)
        return record

    def check_exists(self, model_class, value: Any, column: InstrumentedAttribute, error_msg: str = "Registro existente, operación no permitida"):
        """Verifica existencia de registro relacionado y lanza HTTP 400 si existe."""
        exists = model_class.query.filter(column == value).first()
        if exists:
            raise HTTPException(status_code=400, detail=error_msg)

    