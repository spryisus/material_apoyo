from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserPreferenceBase(BaseModel):
    option_id: Optional[int] = None
    question_id: Optional[int]=None


class UserPreferenceCreate(UserPreferenceBase):
    user_id: int

class UserPreferenceUpdate(UserPreferenceBase):
    pass

class UserPreferenceOut(UserPreferenceBase):
    id: int
    user_id: int
    question_id: int
    option_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    class Config:
        from_attributes = True