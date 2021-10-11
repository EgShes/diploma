from enum import Enum
from typing import List

from pydantic import BaseModel


class EntityType(str, Enum):
    person = "PER"
    location = "LOC"
    organization = "ORG"


class NamedEntity(BaseModel):
    text: str
    type: EntityType

    def __hash__(self) -> int:
        return hash(self.text.lower() + self.type.name)

    def __repr__(self) -> str:
        return f"{self.type.name}:{self.text}"


class NerOutputSchema(BaseModel):
    entities: List[NamedEntity]
