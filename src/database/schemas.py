from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, conint

from src.database.models import EntityType, SentimentType

# source text


class SourceTextBase(BaseModel):
    text: str
    source: str
    employee_id: conint(gt=0)
    chat_id: conint(gt=0)
    published_at: Optional[datetime]


class SourceTextCreate(SourceTextBase):
    pass


class SourceText(SourceTextBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# employee


class EmployeeBase(BaseModel):
    passport: str
    first_name: str
    second_name: str
    third_name: Optional[str]
    department: str

    class Config:
        orm_mode = True


class EmployeeCreate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int
    created_at: datetime
    source_texts: List[SourceText]


# chat


class ChatTypeType(str, Enum):
    direct = "direct"
    group = "group"
    comment = "comments"


class ChatBase(BaseModel):
    type: ChatTypeType

    class Config:
        orm_mode = True


class ChatCreate(ChatBase):
    pass


class Chat(ChatBase):
    id: int
    created_at: datetime


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
