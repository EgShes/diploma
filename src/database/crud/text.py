from typing import List

from sqlalchemy.orm import Session

from src.database import models, schemas
from src.database.crud.chat import get_chat_by_id
from src.database.crud.common import get_by_id, get_by_id_list
from src.database.crud.employee import get_employee_by_id
from src.database.crud.exceptions import NotExistsError
from src.database.crud.processing_status import create_processing_status


def get_source_text_by_id(db: Session, id_: int) -> schemas.SourceText:
    return get_by_id(db, models.SourceText, id_)


def get_source_text_by_ids(db: Session, ids: List[int]) -> List[schemas.SourceText]:
    return get_by_id_list(db, models.SourceText, ids)


def create_source_text(db: Session, source_text: schemas.SourceTextCreate) -> models.SourceText:
    if not get_employee_by_id(db, source_text.employee_id):
        raise NotExistsError(f"Employee with id {source_text.employee_id} not found")
    if not get_chat_by_id(db, source_text.chat_id):
        raise NotExistsError(f"Chat with id {source_text.chat_id} not found")
    db_source_text = models.SourceText(
        text=source_text.text,
        source=source_text.source,
        employee_id=source_text.employee_id,
        chat_id=source_text.chat_id,
        published_at=source_text.published_at,
    )
    db.add(db_source_text)
    db.commit()
    db.refresh(db_source_text)
    create_processing_status(db, db_source_text.id)
    return db_source_text


def get_texts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SourceText).offset(skip).limit(limit).all()
