from pydantic import BaseModel


class CarroCreateDTO(BaseModel):
    brand: str
    model: str
    year: int
    price: int
    

class CarroReadDTO(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    price: int

class CarroUpdateDTO(BaseModel):
    brand: str
    model: str
    price: int
    year: int
    
class CarroResponseDTO(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    price: int

    class Config:
        orm_mode = True