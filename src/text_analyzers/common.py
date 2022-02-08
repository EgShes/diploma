from datetime import datetime, timezone

from pydantic import BaseModel, Field, conlist


class RequestFailedException(Exception):
    pass


class SourceText(BaseModel):
    id: int
    text: str
    source: str


class Payload(BaseModel):
    source_texts: conlist(SourceText, max_items=100)


class Message(BaseModel):
    payload: Payload
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Meta(BaseModel):
    id: int
