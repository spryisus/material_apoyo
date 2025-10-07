from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey,Boolean 
from app.core.db import Base
from sqlalchemy.sql import func

class Comment(Base):
    __tablename__ = "photo_comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_id = Column(Integer, ForeignKey("test.photos.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("test.users.user_id", ondelete="CASCADE"), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("test.users.user_id"))
    updated_by = Column(Integer, ForeignKey("test.users.user_id"))