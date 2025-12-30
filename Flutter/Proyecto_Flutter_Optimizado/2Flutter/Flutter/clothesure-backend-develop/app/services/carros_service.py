from app.core.base_service import BaseService
from app.models.carros import Carro
from app.repositories.carros_repository import CarrosRepository
from sqlalchemy.orm import Session

class CarrosService(BaseService):
    def __init__(self, repository: CarrosRepository, db: Session):
        super().__init__(repository, Carro)
        self.db = db
    