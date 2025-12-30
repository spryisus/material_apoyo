from app.core.basecrud import BaseCRUD
from app.models.user_preference_model import UserPreference
from app.interfaces.user_preference_repository import IUserPreferenceRepository
from typing import Dict, Any, Optional

class UserPreferenceRepository(BaseCRUD[UserPreference], IUserPreferenceRepository):
    def __init__(self, db):
        super().__init__(UserPreference, db)
    
    def get_by_user_id(self, user_id: str) -> Optional[UserPreference]:
        """Obtiene preferencias por ID de usuario."""
        return self.db.query(UserPreference).filter(UserPreference.user_id == user_id).first()
    
    def create_preferences(self, user_id: str, answers: Dict[str, Any], completed_survey: bool = False) -> UserPreference:
        """Crea nuevas preferencias de usuario."""
        preferences = UserPreference(
            user_id=user_id,
            style_personal=answers.get('style_personal'),
            style_personal_custom=answers.get('style_personal_custom'),
            occasions=answers.get('occasions'),
            favorite_items=answers.get('favorite_items'),
            body_shape=answers.get('body_shape'),
            skin_tone=answers.get('skin_tone'),
            fit_preference=answers.get('fit_preference'),
            shoes=answers.get('shoes'),
            accessories=answers.get('accessories'),
            completed_survey=completed_survey
        )
        return self.create(preferences)
    
    def update_preferences(self, user_id: str, answers: Dict[str, Any], completed_survey: bool = True) -> UserPreference:
        """Actualiza preferencias existentes."""
        preferences = self.get_by_user_id(user_id)
        if not preferences:
            raise ValueError(f"Usuario {user_id} no tiene preferencias")
        
        update_data = {
            'style_personal': answers.get('style_personal'),
            'style_personal_custom': answers.get('style_personal_custom'),
            'occasions': answers.get('occasions'),
            'favorite_items': answers.get('favorite_items'),
            'body_shape': answers.get('body_shape'),
            'skin_tone': answers.get('skin_tone'),
            'fit_preference': answers.get('fit_preference'),
            'shoes': answers.get('shoes'),
            'accessories': answers.get('accessories'),
            'completed_survey': completed_survey
        }
        
        return self.update(preferences, update_data)
    
    def has_completed_survey(self, user_id: str) -> bool:
        """Verifica si usuario completó la encuesta."""
        preferences = self.get_by_user_id(user_id)
        return preferences and preferences.completed_survey