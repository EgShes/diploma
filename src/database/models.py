from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.database import Base


class SourceText(Base):
    __tablename__ = "source_text"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    source = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    named_entities = relationship("NamedEntity", back_populates="source_text")


class NamedEntity(Base):
    __tablename__ = "named_entity"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    source_text_id = Column(Integer, ForeignKey("source_text.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    source_text = relationship("SourceText", back_populates="named_entities")
