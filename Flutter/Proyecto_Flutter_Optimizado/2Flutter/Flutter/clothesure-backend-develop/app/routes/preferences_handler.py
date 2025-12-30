"""
Handler para endpoints de preferencias de usuario.
Incluye endpoints para encuesta inicial y gestión de preferencias.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, validator

from app.core.db import get_db
from app.models.preference_questions_model import PreferenceQuestion
from app.models.preference_options_model import PreferenceOption
from app.models.user_preference_model import UserPreference
from app.repositories.preference_questions_repository import PreferenceQuestionsRepository
from app.repositories.preference_options_repository import PreferenceOptionsRepository
from app.repositories.user_preference_repository import UserPreferenceRepository

router = APIRouter()

# DTOs para validación
class SurveyAnswersRequest(BaseModel):
    user_id: str
    answers: Dict[str, Any]
    
    @validator('answers')
    def validate_answers(cls, v):
        # style_personal: requerido
        if 'style_personal' not in v:
            raise ValueError('style_personal es requerido')
        
        # occasions: array no vacío
        if not v.get('occasions') or len(v.get('occasions', [])) == 0:
            raise ValueError('occasions debe tener al menos 1 elemento')
        
        # favorite_items: 1-3 elementos
        items = v.get('favorite_items', [])
        if not items or len(items) < 1 or len(items) > 3:
            raise ValueError('favorite_items debe tener entre 1 y 3 elementos')
        
        # Campos requeridos
        required = ['body_shape', 'skin_tone', 'fit_preference', 'shoes', 'accessories']
        for field in required:
            if field not in v:
                raise ValueError(f'{field} es requerido')
        
        return v

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    question_type: str
    order: int
    max_selections: Optional[int]
    has_illustrations: bool
    has_color_circles: bool
    options: List[Dict[str, Any]]

class SurveyQuestionsResponse(BaseModel):
    success: bool
    questions: List[QuestionResponse]

class SurveyAnswersResponse(BaseModel):
    success: bool
    message: str
    data: Dict[str, Any]

class UserPreferencesResponse(BaseModel):
    success: bool
    has_preferences: bool
    completed_survey: bool
    preferences: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

@router.get("/questions", response_model=SurveyQuestionsResponse)
def get_survey_questions(db: Session = Depends(get_db)):
    """
    Devuelve todas las preguntas de la encuesta con sus opciones.
    Ordena por campo 'order'.
    """
    try:
        # Obtener preguntas ordenadas
        questions_repo = PreferenceQuestionsRepository(db)
        questions = questions_repo.get_all()
        
        # Obtener opciones para cada pregunta
        options_repo = PreferenceOptionsRepository(db)
        
        questions_data = []
        for question in questions:
            options = options_repo.get_by_question_id(question.id)
            options_data = [
                {
                    "id": opt.id,
                    "text": opt.text,
                    "value": opt.value,
                    "requires_text": opt.requires_text
                }
                for opt in options
            ]
            
            question_data = {
                "id": question.id,
                "question_text": question.question_text,
                "question_type": question.question_type,
                "order": question.order,
                "max_selections": question.max_selections,
                "has_illustrations": question.has_illustrations,
                "has_color_circles": question.has_color_circles,
                "options": options_data
            }
            questions_data.append(question_data)
        
        return SurveyQuestionsResponse(
            success=True,
            questions=questions_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener preguntas: {str(e)}")

@router.post("/answers", response_model=SurveyAnswersResponse)
def save_survey_answers(
    request: SurveyAnswersRequest,
    db: Session = Depends(get_db)
):
    """
    Guarda las respuestas de la encuesta inicial.
    Marca completed_survey = True.
    """
    try:
        user_pref_repo = UserPreferenceRepository(db)
        
        # Verificar si usuario ya tiene preferencias
        existing_prefs = user_pref_repo.get_by_user_id(request.user_id)
        
        if existing_prefs and existing_prefs.completed_survey:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "error": "survey_already_completed",
                    "message": "Ya completaste la encuesta. Usa PUT para actualizar."
                }
            )
        
        # Crear o actualizar preferencias
        if existing_prefs:
            # Actualizar existente
            user_pref_repo.update_preferences(
                request.user_id,
                request.answers,
                completed_survey=True
            )
        else:
            # Crear nuevo
            user_pref_repo.create_preferences(
                request.user_id,
                request.answers,
                completed_survey=True
            )
        
        return SurveyAnswersResponse(
            success=True,
            message="Encuesta completada exitosamente",
            data={
                "user_id": request.user_id,
                "completed_survey": True
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar respuestas: {str(e)}")

@router.get("/{user_id}", response_model=UserPreferencesResponse)
def get_user_preferences(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Obtiene las preferencias guardadas de un usuario.
    """
    try:
        user_pref_repo = UserPreferenceRepository(db)
        preferences = user_pref_repo.get_by_user_id(user_id)
        
        if not preferences:
            return UserPreferencesResponse(
                success=True,
                has_preferences=False,
                completed_survey=False,
                message="Usuario debe completar encuesta inicial"
            )
        
        # Mapear preferencias a formato de respuesta
        prefs_data = {
            "style_personal": preferences.style_personal,
            "style_personal_custom": preferences.style_personal_custom,
            "occasions": preferences.occasions,
            "favorite_items": preferences.favorite_items,
            "body_shape": preferences.body_shape,
            "skin_tone": preferences.skin_tone,
            "fit_preference": preferences.fit_preference,
            "shoes": preferences.shoes,
            "accessories": preferences.accessories
        }
        
        return UserPreferencesResponse(
            success=True,
            has_preferences=True,
            completed_survey=preferences.completed_survey,
            preferences=prefs_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener preferencias: {str(e)}")

@router.put("/{user_id}", response_model=SurveyAnswersResponse)
def update_user_preferences(
    user_id: str,
    request: SurveyAnswersRequest,
    db: Session = Depends(get_db)
):
    """
    Actualiza preferencias de un usuario.
    Mantiene completed_survey = True.
    """
    try:
        user_pref_repo = UserPreferenceRepository(db)
        
        # Verificar que usuario existe y tiene preferencias
        existing_prefs = user_pref_repo.get_by_user_id(user_id)
        
        if not existing_prefs:
            raise HTTPException(
                status_code=404,
                detail={
                    "success": False,
                    "error": "preferences_not_found",
                    "message": "Usuario no tiene preferencias. Completa la encuesta primero."
                }
            )
        
        # Actualizar preferencias
        user_pref_repo.update_preferences(
            user_id,
            request.answers,
            completed_survey=True
        )
        
        return SurveyAnswersResponse(
            success=True,
            message="Preferencias actualizadas exitosamente",
            data={
                "user_id": user_id,
                "completed_survey": True
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar preferencias: {str(e)}")
