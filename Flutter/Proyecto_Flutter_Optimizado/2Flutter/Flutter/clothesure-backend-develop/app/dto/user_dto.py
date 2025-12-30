from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    profile_picture_url: Optional[str] = None
    bio: Optional[str] = None
    is_private: Optional[bool] = False


class UserOut(BaseModel):
    user_id: int
    username: str
    email: str
    bio: Optional[str] = None
    is_private: bool
    registration_date: datetime
    created_at: datetime
    updated_at: datetime
    profile_picture_url: Optional[str] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    profile_picture_url: Optional[str] = None
    bio: Optional[str] = None
    is_private: Optional[bool] = None

class PasswordResetRequest(BaseModel):
    token: str
    new_password: str

    model_config = {
        "from_attributes": True
    }
 
class UserLogin(BaseModel):
    email: EmailStr
    password: str   

class UserInPost(BaseModel):
    user_id: int
    username: str
    profile_picture_url: Optional[str] = None
