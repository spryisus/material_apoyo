from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.dto.photo_dto import PhotoOut 
from app.dto.user_dto import UserInPost


class PostBase(BaseModel):
    ocation: Optional[str] = None
    location: Optional[str] = None
    style: Optional[str] = None
    hide_location: Optional[bool] = False 
    hide_votes: Optional[bool] = False     
    hide_comments: Optional[bool] = False  

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostOut(PostBase):
    id: int
    user_id: int
    user: UserInPost 
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    images: List[PhotoOut]

    class Config:
        from_attributes = True
