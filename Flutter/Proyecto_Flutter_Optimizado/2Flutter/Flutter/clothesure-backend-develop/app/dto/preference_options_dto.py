from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PreferenceOptionBase(BaseModel):
    option_text: str
    value_code: Optional[str] = None

class PreferenceOptionCreate(PreferenceOptionBase):
    question_id: int

class PreferenceOptionUpdate(PreferenceOptionBase):
    question_id: Optional[int] = None

class PreferenceOptionOut(PreferenceOptionBase):
    id: int
    question_id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    class Config:
        from_attributes = True
