import enum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_mixin, declared_attr, relationship
from sqlalchemy.sql import func

from src.database.database import Base


class EntityType(str, enum.Enum):
    person = "PER"
    location = "LOC"
    organization = "ORG"


class SentimentType(str, enum.Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"
    skip = "skip"
    speech = "speech"


class ProcessingStatusType(str, enum.Enum):
    not_processed = "not_processed"
    processing = "processing"
    processed = "processed"


class ChatType(str, enum.Enum):
    direct = "direct"
    group = "group"
    comment = "comments"


class SourceText(Base):
    __tablename__ = "source_text"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    source = Column(String, nullable=False)
    published_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)
    author = relationship("Employee", back_populates="source_texts")

    chat_id = Column(Integer, ForeignKey("chat.id"), nullable=False)
    chat = relationship("Chat", back_populates="source_texts")

    named_entities = relationship("NamedEntity", back_populates="source_text")
    words = relationship("SourceTextWordAssociation", back_populates="source_text")
    sentiments = relationship("Sentiment", back_populates="source_text")

    word_processing_status = relationship("WordProcessingStatus", back_populates="source_text")
    named_entity_processing_status = relationship("NamedEntityProcessingStatus", back_populates="source_text")
    sentiment_processing_status = relationship("SentimentProcessingStatus", back_populates="source_text")


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    passport = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    third_name = Column(String, nullable=True)
    department = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    source_texts = relationship("SourceText", back_populates="author")
    chats = relationship("EmployeeChatAssociation", back_populates="employee")


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(ChatType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    source_texts = relationship("SourceText", back_populates="chat")
    employees = relationship("EmployeeChatAssociation", back_populates="chat")


class EmployeeChatAssociation(Base):
    __tablename__ = "employee_chart"
    chat_id = Column(ForeignKey("chat.id"), primary_key=True)
    employee_id = Column(ForeignKey("employee.id"), primary_key=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    employee = relationship("Employee", back_populates="chats")
    chat = relationship("Chat", back_populates="employees")


class NamedEntity(Base):
    __tablename__ = "named_entity"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    type = Column(Enum(EntityType), nullable=False)
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
    text = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    source_texts = relationship("SourceTextWordAssociation", back_populates="word")


class Sentiment(Base):
    __tablename__ = "sentiment"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(SentimentType), nullable=False)
    probability = Column(Float, nullable=False)
    source_text_id = Column(Integer, ForeignKey("source_text.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    source_text = relationship("SourceText", back_populates="sentiments")


@declarative_mixin
class ProcessingStatus:

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(ProcessingStatusType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    @declared_attr
    def source_text_id(cls):
        return Column(Integer, ForeignKey("source_text.id"), nullable=False)


class WordProcessingStatus(ProcessingStatus, Base):
    __tablename__ = "word_processing_status"

    source_text = relationship("SourceText", back_populates="word_processing_status")


class NamedEntityProcessingStatus(ProcessingStatus, Base):
    __tablename__ = "named_entity_processing_status"

    source_text = relationship("SourceText", back_populates="named_entity_processing_status")


class SentimentProcessingStatus(ProcessingStatus, Base):
    __tablename__ = "sentiment_processing_status"

    source_text = relationship("SourceText", back_populates="sentiment_processing_status")
