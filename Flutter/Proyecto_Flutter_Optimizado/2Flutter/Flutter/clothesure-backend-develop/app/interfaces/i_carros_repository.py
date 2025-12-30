from typing import Protocol, Any
from sqlalchemy.orm.attributes import InstrumentedAttribute
from app.models.carros import Carro

class ICarrosRepository(Protocol):
    def create(self, obj: Carro) -> Carro:
        ...

    def get(self, value: Any, column: InstrumentedAttribute) -> Carro | None:
        ...

    def get_where(self, *conditions: Any) -> list[Carro]:
        ...

    def get_all(self) -> list[Carro]:
        ...

    def update(self, obj: Carro, data: dict) -> Carro | None:
        ...

    def delete(self, value: Any, column: InstrumentedAttribute) -> bool:
        ...
