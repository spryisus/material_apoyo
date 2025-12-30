from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PhotoBase(BaseModel):
    url: str
    order_index: Optional[int] = 1

class PhotoCreate(PhotoBase):
    post_id: int

class PhotoUpdate(PhotoBase):
    url: Optional[str] = None
    order_index: Optional[int] = None

class PhotoOut(PhotoBase):
    id: int
    post_id: int
    reactions_count: int
    comments_count: int
    views_count: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None


    class Config:
        from_attributes = True
