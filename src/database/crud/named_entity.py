from sqlalchemy.orm import Session

from src.database import models, schemas
from src.database.crud.processing_status import update_processing_status


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
