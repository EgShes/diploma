from typing import Optional

from sqlmodel import Field, SQLModel


class TextBase(SQLModel):
    raw_text: Optional[str]
    source: Optional[str]


class Text(TextBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class TextCreate(TextBase):
    pass


class TextRead(TextBase):
    id: int
