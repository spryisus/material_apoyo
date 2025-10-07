from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import JSONResponse
from app.dto.preference_options_dto import PreferenceOptionCreate, PreferenceOptionUpdate, PreferenceOptionOut
from app.factories.repository_factory import get_preference_options_service
from app.security.dependencies import get_current_user
from app.core.db import get_db

router = APIRouter(prefix="/preference-options", tags=["Preference Options"])

@router.post("/", response_model=PreferenceOptionOut, status_code=status.HTTP_201_CREATED)
def create_preference_option(
    data: PreferenceOptionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_preference_options_service(db)
    return service.create(data.dict(), current_user.user_id)

@router.get("/", response_model=List[PreferenceOptionOut])
def list_preference_options(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_preference_options_service(db)
    return service.list_all()

@router.get("/{option_id}", response_model=PreferenceOptionOut)
def get_preference_option(
    option_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_preference_options_service(db)
    obj = service.get(option_id, service.repo.model.id)
    if not obj:
        raise HTTPException(status_code=404, detail="Opción no encontrada")
    return obj

@router.put("/{option_id}", response_model=PreferenceOptionOut)
def update_preference_option(
    option_id: int,
    data: PreferenceOptionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_preference_options_service(db)
    updated_obj = service.update(option_id, service.repo.model.id, data.dict(exclude_unset=True), current_user.user_id)
    if not updated_obj:
        raise HTTPException(status_code=404, detail="Opción no encontrada")
    return updated_obj

@router.delete("/{option_id}", status_code=status.HTTP_200_OK)
def delete_preference_option(
    option_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_preference_options_service(db)
    try:
        service.delete(option_id, service.repo.model.id)
        return JSONResponse(content={"message": "Opción eliminada correctamente."})
    except HTTPException as e:
        if e.status_code == 403:
            return JSONResponse(status_code=403, content={"message": "No tienes permiso para eliminar esta opción."})
        elif e.status_code == 404:
            return JSONResponse(status_code=404, content={"message": "Opción no encontrada."})
        raise e
