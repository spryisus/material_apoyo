from app.core.base_service import BaseService
from app.models.photo_model import Photo
from app.repositories.photo_repository import PhotoModel
from sqlalchemy.orm import Session

class PhotoService(BaseService):
    def __init__(self, repository: PhotoModel, db: Session):
        super().__init__(repository, Photo)
        self.db = db