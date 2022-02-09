from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.database.models import EntityType, SentimentType

# source text


class SourceTextBase(BaseModel):
    text: str
    source: str


class SourceTextCreate(SourceTextBase):
    pass


class SourceText(SourceTextBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# named entity


class NamedEntityBase(BaseModel):
    text: str
    type: EntityType


class NamedEntityCreate(NamedEntityBase):
    pass


class NamedEntity(NamedEntityBase):
    id: int
    created_at: datetime
    source_text_id: int

    class Config:
        orm_mode = True


# word


class WordBase(BaseModel):
    text: str


class WordCreate(WordBase):
    quantity: int


class Word(WordBase):
    id: int
    created_at: datetime
    source_text_ids: List[int]

    class Config:
        orm_mode = True


# sentiment


class SentimentBase(BaseModel):
    type: SentimentType
    probability: float


class SentimentCreate(SentimentBase):
    pass


class Sentiment(SentimentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
