from datetime import datetime
from typing import List

from pydantic import BaseModel


class SourceTextBase(BaseModel):
    text: str
    source: str


class SourceTextCreate(SourceTextBase):
    pass


class SourceText(SourceTextBase):
    id: int
    named_entities: List[str]
    created_at: datetime

    class Config:
        orm_mode = True
