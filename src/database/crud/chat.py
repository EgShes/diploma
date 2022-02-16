from typing import List

from sqlalchemy.orm import Session

from src.database import models, schemas
from src.database.crud.common import get_by_id, get_by_id_list


def get_chat_by_id(db: Session, id_: int) -> schemas.Chat:
    return get_by_id(db, models.Chat, id_)


def get_chat_by_ids(db: Session, ids: List[int]) -> List[schemas.Chat]:
    return get_by_id_list(db, models.Chat, ids)


def create_chat(db: Session, chat: schemas.ChatCreate) -> models.Chat:
    chat_db = models.Chat(type=chat.type)
    db.add(chat_db)
    db.commit()
    db.refresh(chat_db)
    return chat_db
