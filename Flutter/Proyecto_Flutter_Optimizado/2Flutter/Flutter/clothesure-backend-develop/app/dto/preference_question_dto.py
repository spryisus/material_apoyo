from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.dto.preference_options_dto import PreferenceOptionOut

class PreferenceQuestionBase(BaseModel):
    question_text: str
    category: Optional[str] = None
    is_active: Optional[bool] = True

class PreferenceQuestionCreate(PreferenceQuestionBase):
    pass

class PreferenceQuestionUpdate(PreferenceQuestionBase):
    pass

class PreferenceQuestionOut(PreferenceQuestionBase):
    id: int
    options: List[PreferenceOptionOut] = []
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    

    class Config:
        from_attributes = True