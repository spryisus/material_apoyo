from app.core.basecrud import BaseCRUD
from app.models.post_model import Post
from app.interfaces.post_repository import IPostRepository

class PostModel(BaseCRUD[Post], IPostRepository):
    def __init__(self, db):
        super().__init__(Post, db)
