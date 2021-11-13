from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.database.models import EntityType


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


class SourceTextBase(BaseModel):
    text: str
    source: str


class SourceTextCreate(SourceTextBase):
    pass


class SourceText(SourceTextBase):
    id: int
    named_entities: List[NamedEntity]
    created_at: datetime

    class Config:
        orm_mode = True
