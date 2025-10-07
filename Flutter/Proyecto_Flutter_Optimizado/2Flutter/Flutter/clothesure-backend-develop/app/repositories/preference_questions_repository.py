from app.core.basecrud import BaseCRUD
from app.models.preference_questions_model import PreferenceQuestion
from app.interfaces.preference_questions_repository import IPreferenceQuestionRepository
from typing import List

class PreferenceQuestionsRepository(BaseCRUD[PreferenceQuestion], IPreferenceQuestionRepository):
    def __init__(self, db):
        super().__init__(PreferenceQuestion, db)
    
    def get_by_order(self, order: int) -> PreferenceQuestion:
        """Obtiene pregunta por orden."""
        return self.db.query(PreferenceQuestion).filter(PreferenceQuestion.order == order).first()
    
    def get_ordered(self) -> List[PreferenceQuestion]:
        """Obtiene todas las preguntas ordenadas por campo 'order'."""
        return self.db.query(PreferenceQuestion).order_by(PreferenceQuestion.order).all()