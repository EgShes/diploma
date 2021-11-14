import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.database import Base


class EntityType(str, enum.Enum):
    person = "PER"
    location = "LOC"
    organization = "ORG"


class SourceText(Base):
    __tablename__ = "source_text"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    source = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    named_entities = relationship("NamedEntity", back_populates="source_text")
    words = relationship("SourceTextWordAssociation", back_populates="source_text")


class NamedEntity(Base):
    __tablename__ = "named_entity"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    type = Column(Enum(EntityType))
    source_text_id = Column(Integer, ForeignKey("source_text.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    source_text = relationship("SourceText", back_populates="named_entities")


class SourceTextWordAssociation(Base):
    __tablename__ = "word_source_text"

    source_text_id = Column(ForeignKey("source_text.id"), primary_key=True)
    word_id = Column(ForeignKey("word.id"), primary_key=True)
    quantity = Column(Integer, default=1, nullable=False)

    source_text = relationship("SourceText", back_populates="words")
    word = relationship("Word", back_populates="source_texts")


class Word(Base):
    __tablename__ = "word"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    source_texts = relationship("SourceTextWordAssociation", back_populates="word")
