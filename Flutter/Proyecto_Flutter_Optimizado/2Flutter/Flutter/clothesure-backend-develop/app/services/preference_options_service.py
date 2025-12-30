from app.core.base_service import BaseService
from app.models.preference_options_model import PreferenceOption
from app.repositories.preference_options_repository import PreferenceOptionsRepository
from sqlalchemy.orm import Session

class  PreferenceOptionService(BaseService):
    def __init__(self, repository: PreferenceOptionsRepository):
        super().__init__(repository,  PreferenceOption)
