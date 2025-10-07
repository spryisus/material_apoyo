from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import JSONResponse
from app.dto.user_device_dto import UserDeviceCreate, UserDeviceUpdate, UserDeviceOut
from app.factories.repository_factory import get_user_device_service
from app.security.dependencies import get_current_user
from app.core.db import get_db

router = APIRouter(prefix="/user-devices", tags=["User Devices"])

@router.post("/", response_model=UserDeviceOut, status_code=status.HTTP_201_CREATED)
def create_user_device(
    data: UserDeviceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_user_device_service(db)
    return service.create(data.dict(), current_user.user_id)

@router.get("/", response_model=List[UserDeviceOut])
def list_user_devices(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_user_device_service(db)
    return service.list_all()

@router.get("/{device_id}", response_model=UserDeviceOut)
def get_user_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_user_device_service(db)
    obj = service.get(device_id, service.repo.model.id)
    if not obj:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return obj

@router.put("/{device_id}", response_model=UserDeviceOut)
def update_user_device(
    device_id: int,
    data: UserDeviceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_user_device_service(db)
    updated_device = service.update(device_id, service.repo.model.id, data.dict(exclude_unset=True), current_user.user_id)
    if not updated_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return updated_device

@router.delete("/{device_id}", status_code=status.HTTP_200_OK)
def delete_user_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = get_user_device_service(db)
    try:
        service.delete(device_id, service.repo.model.id)
        return JSONResponse(content={"message": "Dispositivo eliminado correctamente."})
    except HTTPException as e:
        if e.status_code == 403:
            return JSONResponse(status_code=403, content={"message": "No tienes permiso para eliminar este dispositivo."})
        elif e.status_code == 404:
            return JSONResponse(status_code=404, content={"message": "Dispositivo no encontrado."})
        raise e