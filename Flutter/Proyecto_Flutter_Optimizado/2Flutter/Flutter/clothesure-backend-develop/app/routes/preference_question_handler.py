from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import JSONResponse
from app.dto.preference_question_dto import PreferenceQuestionCreate, PreferenceQuestionUpdate, PreferenceQuestionOut
from app.factories.repository_factory import get_preference_question_service
from app.security.dependencies import get_current_user
from app.core.db import get_db
from app.models.preference_questions_model import PreferenceQuestion
from app.models.preference_options_model import PreferenceOption

router = APIRouter(prefix="/preference-questions", tags=["Preference Questions"])

@router.post("/", response_model=PreferenceQuestionOut, status_code=status.HTTP_201_CREATED)
def create_preference_question(
    data: PreferenceQuestionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_preference_question_service(db)
    return service.create(data.dict(), current_user.user_id)


@router.get("/", response_model=List[PreferenceQuestionOut])
def list_preference_questions(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    questions = db.query(PreferenceQuestion).filter(PreferenceQuestion.is_active == True).all()
    options = db.query(PreferenceOption).filter(PreferenceOption.question_id.in_([q.id for q in questions])).all()
    options_by_question = {}
    for opt in options:
        options_by_question.setdefault(opt.question_id, []).append(opt)
    result = []
    for q in questions:
        q_dict = q.__dict__.copy()
        q_dict['options'] = options_by_question.get(q.id, [])
        result.append(q_dict)

    return result

@router.get("/{question_id}", response_model=PreferenceQuestionOut)
def get_preference_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_preference_question_service(db)
    obj = service.get(question_id, service.repo.model.id)
    if not obj:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    obj.options
    return obj

@router.put("/{question_id}", response_model=PreferenceQuestionOut)
def update_preference_question(
    question_id: int,
    data: PreferenceQuestionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_preference_question_service(db)
    updated_obj = service.update(question_id, service.repo.model.id, data.dict(exclude_unset=True), current_user.user_id)
    if not updated_obj:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    updated_obj.options
    return updated_obj
@router.delete("/{question_id}", status_code=status.HTTP_200_OK)
def delete_preference_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_preference_question_service(db)
    try:
        service.delete(question_id, service.repo.model.id)
        return JSONResponse(content={"message": "Pregunta eliminada correctamente."})
    except HTTPException as e:
        if e.status_code == 403:
            return JSONResponse(status_code=403, content={"message": "No tienes permiso para eliminar esta pregunta."})
        elif e.status_code == 404:
            return JSONResponse(status_code=404, content={"message": "Pregunta no encontrada."})
        raise e
