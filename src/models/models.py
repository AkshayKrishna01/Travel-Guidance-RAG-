from sqlalchemy import Column, Integer, text, DateTime, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
# models/models.py
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector 

Base = declarative_base()

# EMBED_DIM = 1024  
class KnowledgeBase(Base):
    __tablename__ = "akshay_embedding_data"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    vector_points = Column(Vector(1024), nullable=False)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(String, default="admin")
    updated_by = Column(String, default="admin")
    is_active = Column(Boolean, default=True)
