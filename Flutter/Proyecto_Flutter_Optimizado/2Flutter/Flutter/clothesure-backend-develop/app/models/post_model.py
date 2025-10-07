from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from app.core.db import Base
from sqlalchemy.sql import func

class Post(Base):
    __tablename__ = "posts"

    # Campos existentes (sin cambios)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    ocation = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    style = Column(String(255), nullable=True)
    hide_location = Column(Boolean, nullable=False, default=False)
    hide_votes = Column(Boolean, nullable=False, default=False)
    hide_comments = Column(Boolean, nullable=False, default=False)
    # style_tags = Column(JSON, nullable=True)  # Comentado porque no existe en la DB real
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)