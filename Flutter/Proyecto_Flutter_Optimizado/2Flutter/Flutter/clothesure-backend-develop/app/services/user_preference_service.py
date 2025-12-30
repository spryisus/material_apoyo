from app.core.base_service import BaseService
from app.models.user_preference_model import UserPreference
from app.repositories.user_preference_repository import UserPreferenceRepository
from sqlalchemy.orm import Session

class UserPreferenceService(BaseService):
    def __init__(self, repository: UserPreferenceRepository):
        super().__init__(repository, UserPreference)
