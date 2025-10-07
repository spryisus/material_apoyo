from app.core.basecrud import BaseCRUD
from app.models.user_model import User
from app.interfaces.user_repository import IUserRepository

class UserModel(BaseCRUD[User], IUserRepository):
    def __init__(self, db):
        super().__init__(User, db)
