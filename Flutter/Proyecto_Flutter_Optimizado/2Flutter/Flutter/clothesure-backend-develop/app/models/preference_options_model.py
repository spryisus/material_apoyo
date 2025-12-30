from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.core.db import Base

class PreferenceOption(Base):
    __tablename__ = "preference_options"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("preference_questions.id", ondelete="CASCADE"), nullable=False)
    text = Column(String(200), nullable=False)  # Texto mostrado al usuario
    value = Column(String(100), nullable=False)  # Valor almacenado (snake_case)
    requires_text = Column(Boolean, default=False)  # Si requiere input de texto adicional
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)