from typing import List

from sqlalchemy.orm import Session

from src.database import models, schemas
from src.database.crud.common import get_by_id, get_by_id_list
from src.database.crud.processing_status import (
    get_oldest_not_processed,
    update_processing_status,
)


def create_named_entity(
    db: Session, source_text_id: int, named_entity: schemas.NamedEntityCreate
) -> models.NamedEntity:
    db_named_entity = models.NamedEntity(text=named_entity.text, type=named_entity.type, source_text_id=source_text_id)
    db.add(db_named_entity)
    db.commit()
    db.refresh(db_named_entity)
    update_processing_status(
        db, models.NamedEntityProcessingStatus, source_text_id, models.ProcessingStatusType.processed
    )
    return db_named_entity


def get_named_entity_by_id(db: Session, id_: int) -> schemas.NamedEntity:
    return get_by_id(db, models.NamedEntity, id_)


def get_named_entity_by_ids(db: Session, ids: List[int]) -> List[schemas.NamedEntity]:
    return get_by_id_list(db, models.NamedEntity, ids)


def get_oldest_not_processed_named_entities(db: Session, n: int) -> List[int]:
    source_text_ids = get_oldest_not_processed(db, models.NamedEntityProcessingStatus, n)
    if len(source_text_ids) != 0:
        update_processing_status(
            db, models.NamedEntityProcessingStatus, source_text_ids, models.ProcessingStatusType.processing
        )
    return source_text_ids
