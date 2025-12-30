from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import JSONResponse
from app.dto.user_preference_dto import UserPreferenceCreate, UserPreferenceUpdate, UserPreferenceOut
from app.factories.repository_factory import get_user_preference_service
from app.security.dependencies import get_current_user
from app.core.db import get_db

router = APIRouter(prefix="/user-preferences", tags=["User Preferences"])

@router.post("/", response_model=UserPreferenceOut, status_code=status.HTTP_201_CREATED)
def save_user_preference(
    data: UserPreferenceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_user_preference_service(db)
    existing = service.get_or_none(data.question_id, service.repo.model.question_id)
    if existing and existing.user_id == data.user_id:
        updated_obj = service.update(existing.id, service.repo.model.id, data.dict(exclude_unset=True), current_user.user_id)
        return updated_obj
    return service.create(data.dict(), current_user.user_id)

@router.get("/", response_model=List[UserPreferenceOut])
def list_user_preferences(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_user_preference_service(db)
    return service.get_where(service.repo.model.user_id == current_user.user_id)

@router.get("/{preference_id}", response_model=UserPreferenceOut)
def get_user_preference(
    preference_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_user_preference_service(db)
    obj = service.get_or_404(preference_id, service.repo.model.id)
    return obj

@router.put("/{preference_id}", response_model=UserPreferenceOut)
def update_user_preference(
    preference_id: int,
    data: UserPreferenceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_user_preference_service(db)
    updated_obj = service.update(preference_id, service.repo.model.id, data.dict(exclude_unset=True), current_user.user_id)
    if not updated_obj:
        raise HTTPException(status_code=404, detail="Respuesta no encontrada")
    return updated_obj

@router.delete("/{preference_id}", status_code=status.HTTP_200_OK)
def delete_user_preference(
    preference_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_user_preference_service(db)
    try:
        service.delete(preference_id, service.repo.model.id)
        return JSONResponse(content={"message": "Respuesta eliminada correctamente."})
    except HTTPException as e:
        if e.status_code == 403:
            return JSONResponse(status_code=403, content={"message": "No tienes permiso para eliminar esta respuesta."})
        elif e.status_code == 404:
            return JSONResponse(status_code=404, content={"message": "Respuesta no encontrada."})
        raise e
