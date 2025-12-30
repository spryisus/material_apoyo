from app.core.basecrud import BaseCRUD
from app.models.carros import Carro
from app.interfaces.i_carros_repository import ICarrosRepository

class CarrosRepository(BaseCRUD[Carro], ICarrosRepository):
    def __init__(self, db):
        super().__init__(Carro, db)
