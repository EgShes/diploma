from typing import Any, List

from pydantic import BaseModel
from sqlalchemy.orm import Session


def get_by_id(db: Session, model: Any, id_: int) -> BaseModel:
    return db.query(model).filter(model.id == id_).first()


def get_by_id_list(db: Session, model: Any, ids: List[int]) -> List[BaseModel]:
    return db.query(model).filter(model.id.in_(ids)).all()
