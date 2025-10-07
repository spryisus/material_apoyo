from app.core.basecrud import BaseCRUD
from app.models.photo_model import Photo
from app.interfaces.photo_repository import IPhotoRepository

class PhotoModel(BaseCRUD[Photo], IPhotoRepository):
    def __init__(self, db):
        super().__init__(Photo, db)
