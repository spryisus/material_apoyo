from app.core.base_service import BaseService
from app.models.preference_questions_model import PreferenceQuestion
from app.repositories.preference_questions_repository import PreferenceQuestionsRepository
from sqlalchemy.orm import Session

class  PreferenceOptionService(BaseService):
    def __init__(self, repository: PreferenceQuestionsRepository):
        super().__init__(repository,  PreferenceQuestion)
