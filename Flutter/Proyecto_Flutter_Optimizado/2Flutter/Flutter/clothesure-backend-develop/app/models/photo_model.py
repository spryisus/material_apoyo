from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey,Boolean 
from app.core.db import Base
from sqlalchemy.sql import func

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    post_id= Column(Integer, ForeignKey("posts.id"), nullable=False)
    url = Column(Text, nullable=True)
    order_index = Column(Integer, nullable=False)
    reactions_count = Column(Integer, nullable=True, default=0)
    comments_count = Column(Integer, nullable=True, default=0)
    views_count = Column(Integer, nullable=True, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)