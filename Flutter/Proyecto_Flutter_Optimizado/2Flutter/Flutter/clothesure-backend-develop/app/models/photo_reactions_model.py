# app/dto/photo_dto.py
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, func
from app.core.db import Base
from sqlalchemy.sql import func

class PhotoReaction(Base):
    __tablename__ = "photo_reactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_id = Column(Integer, ForeignKey("test.photos.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("test.users.user_id", ondelete="CASCADE"), nullable=False)
    reaction_type_id = Column(Integer, ForeignKey("test.reaction_types.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("test.users.user_id"))
    updated_by = Column(Integer, ForeignKey("test.users.user_id"))

