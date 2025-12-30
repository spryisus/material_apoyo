from app.core.base_service import BaseService
from app.models.post_model import Post
from app.repositories.post_repository import PostModel
from sqlalchemy.orm import Session

class PostService(BaseService):
    def __init__(self, repository: PostModel, db: Session):
        super().__init__(repository, Post)
        self.db = db