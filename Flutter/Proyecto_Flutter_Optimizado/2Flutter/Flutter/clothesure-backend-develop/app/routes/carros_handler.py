from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.dto.carros_dto import CarroCreateDTO, CarroUpdateDTO, CarroResponseDTO
from app.models.carros import Carro
from typing import Optional
from fastapi import Query
from app.factories.repository_factory import  get_carros_service
router = APIRouter(prefix="/carros", tags=["Carros"])

#create, read, update, delete
@router.post("/", response_model=CarroResponseDTO)
def create_carro(data: CarroCreateDTO, db: Session = Depends(get_db)):
    service = get_carros_service(db)
    return service.create(data.dict())

#consultas personalizadas
@router.get("/get_where", response_model=list[CarroResponseDTO])
def buscar_carros(
    brand: Optional[str] = Query(None, description="Marca del carro"),
    year: Optional[int] = Query(None, description="Año del carro"),
    precio_min: Optional[float] = Query(None, description="Precio mínimo"),
    precio_max: Optional[float] = Query(None, description="Precio máximo"),
    db: Session = Depends(get_db)
):
    service = get_carros_service(db)

    condiciones = []
    if brand:
        condiciones.append(Carro.brand == brand)
    if year:
        condiciones.append(Carro.year == year)
    if precio_min is not None:
        condiciones.append(Carro.price >= precio_min)
    if precio_max is not None:
        condiciones.append(Carro.price <= precio_max)

    carros = service.get_where(*condiciones) if condiciones else service.list_all()

    if not carros:
        raise HTTPException(status_code=404, detail="No se encontraron carros con esos filtros")

    return carros

@router.get("/{carro_id}", response_model=CarroResponseDTO)
def get_carro(carro_id: int, db: Session = Depends(get_db)):
    service = get_carros_service(db)
    carro = service.get(carro_id, Carro.id)
    if not carro:
        raise HTTPException(status_code=404, detail="Carro no encontrado")
    return carro

@router.get("/", response_model=list[CarroResponseDTO])
def list_carros(db: Session = Depends(get_db)):
    service = get_carros_service(db)
    return service.list_all()

@router.put("/{carro_id}", response_model=CarroResponseDTO)
def update_carro(carro_id: int, data: CarroUpdateDTO, db: Session = Depends(get_db)):
    service = get_carros_service(db)
    carro = service.update(carro_id, Carro.id, data.dict(exclude_unset=True))
    if not carro:
        raise HTTPException(status_code=404, detail="Carro no encontrado")
    return carro

@router.delete("/{carro_id}")
def delete_carro(carro_id: int, db: Session = Depends(get_db)):
    service = get_carros_service(db)
    deleted = service.delete(carro_id, Carro.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Carro no encontrado")
    return {"message": "Carro eliminado"}

