from sqlalchemy.orm import Session
from app.core.base_service import BaseService
from app.models.user_model import User
from passlib.context import CryptContext
from app.repositories.user_repository import UserModel
from app.security.jwt import create_access_token
from typing import Dict, Any
from fastapi import HTTPException
from jose import jwt, JWTError
from app.core.db import SECRET_KEY, ALGORITHM
from fastapi import HTTPException
from datetime import datetime, timedelta
from app.services.audit_service import set_audit_fields  


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class UserService(BaseService):
    def __init__(self, repository: UserModel): 
        super().__init__(repository, User)
        
    def register_user(self, db: Session, data: Dict) -> User:
        existing = self.repo.get(data["email"], self.model_class.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        data["password"] = pwd_context.hash(data["password"])

        
        new_user = self.model_class(**data)
        db.add(new_user)
        db.flush()  
        set_audit_fields(new_user, user_id=new_user.user_id, is_create=True)

        db.commit()
        db.refresh(new_user)

        return new_user

    def get_user_by_email(self, email: str) -> User:
        user = self.repo.get(email, self.model_class.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        user = self.repo.get(email, self.model_class.email)
        if not user or not pwd_context.verify(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token(data={"sub": str(user.user_id)})
        return {
        "user_id": user.user_id,
        "email": user.email,
        "full_name": user.username,
        "access_token": token,
        "token_type": "bearer"
        }
    
    
    def generate_password_reset_token(self, email: str) -> str:
        user = self.repo.get(email, self.model_class.email)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        expire = datetime.utcnow() + timedelta(hours=1)
        payload = {"sub": email, "exp": expire}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token

    def reset_password_with_token(self, db: Session, token: str, new_password: str) -> User:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if not email:
                raise HTTPException(status_code=400, detail="Token inválido")
        except JWTError:
            raise HTTPException(status_code=400, detail="Token inválido o expirado")

        user = self.repo.get(email, self.model_class.email)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        user.password = pwd_context.hash(new_password)
        db.commit()
        db.refresh(user)
        return user
    
    def get_current_user_from_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token")
            user = self.repo.get(user_id, self.model_class.user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return {"user_id": user.user_id, "email": user.email, "full_name": user.full_name}
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def update_password(self, db: Session, user_id: int, old_password: str, new_password: str) -> User:
        user = self.repo.get(user_id, self.model_class.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if not self.verify_password(old_password, user.password):
            raise HTTPException(status_code=400, detail="La contraseña actual es incorrecta")
        user.password = pwd_context.hash(new_password)
        set_audit_fields(user, user_id=user.user_id, is_create=False)

        db.commit()
        db.refresh(user)
        return user