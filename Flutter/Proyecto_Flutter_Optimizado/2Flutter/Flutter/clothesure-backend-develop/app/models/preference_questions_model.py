from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.core.db import Base

class PreferenceQuestion(Base):
    __tablename__ = "preference_questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)  # 'single' o 'multiple'
    order = Column(Integer, nullable=False, unique=True)  # Orden de aparición
    max_selections = Column(Integer, nullable=True)  # Máximo de selecciones
    has_illustrations = Column(Boolean, default=False)  # Si requiere ilustraciones
    has_color_circles = Column(Boolean, default=False)  # Si requiere círculos de color
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)