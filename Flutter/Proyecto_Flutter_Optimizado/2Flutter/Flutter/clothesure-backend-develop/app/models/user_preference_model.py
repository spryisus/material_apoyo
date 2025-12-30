from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.sql import func
from app.core.db import Base

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(100), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    style_personal = Column(String(50), nullable=True)  # Estilo seleccionado
    style_personal_custom = Column(String(200), nullable=True)  # Texto libre si eligió "otro"
    occasions = Column(JSON, nullable=True)  # Array de ocasiones
    favorite_items = Column(JSON, nullable=True)  # Array de 1-3 prendas favoritas
    body_shape = Column(String(50), nullable=True)  # Forma del cuerpo
    skin_tone = Column(String(50), nullable=True)  # Tono de piel
    fit_preference = Column(String(50), nullable=True)  # Preferencia de ajuste
    shoes = Column(JSON, nullable=True)  # Array de tipos de calzado
    accessories = Column(String(50), nullable=True)  # Frecuencia de uso de accesorios
    completed_survey = Column(Boolean, default=False)  # Si completó la encuesta
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)