from app.core.basecrud import BaseCRUD
from app.models.preference_options_model import PreferenceOption
from app.interfaces.preference_options_repository import IPreferenceOptionRepository
from typing import List

class PreferenceOptionsRepository(BaseCRUD[PreferenceOption], IPreferenceOptionRepository):
    def __init__(self, db):
        super().__init__(PreferenceOption, db)
    
    def get_by_question_id(self, question_id: int) -> List[PreferenceOption]:
        """Obtiene opciones por ID de pregunta."""
        return self.db.query(PreferenceOption).filter(PreferenceOption.question_id == question_id).all()
    
    def get_by_value(self, value: str) -> PreferenceOption:
        """Obtiene opción por valor."""
        return self.db.query(PreferenceOption).filter(PreferenceOption.value == value).first()
