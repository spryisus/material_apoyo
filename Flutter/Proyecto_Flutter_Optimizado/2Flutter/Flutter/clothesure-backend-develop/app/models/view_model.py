from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey,Boolean 
from app.core.db import Base
from sqlalchemy.sql import func

class View(Base):
    __tablename__ = "photo_views"

    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_id = Column(Integer, ForeignKey("test.photos.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("test.users.user_id"))
    viewed_at = Column(DateTime(timezone=True), server_default=func.now())