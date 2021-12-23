from typing import List, Type

from sqlalchemy.orm import Session

from src.database import models


def create_processing_status(db: Session, id_: int):
    for Model in [models.WordProcessingStatus, models.NamedEntityProcessingStatus, models.SentimentProcessingStatus]:
        db_processing_status = Model(status=models.ProcessingStatusType.not_processed, source_text_id=id_)
        db.add(db_processing_status)
    db.commit()


def update_processing_status(
    db: Session, model: Type[models.ProcessingStatus], id_: int, status: models.ProcessingStatusType
):
    db_processing_status = db.query(model).filter(model.source_text_id == id_).first()
    db_processing_status.status = status
    db.commit()


def get_oldest_not_processed(db: Session, model: Type[models.ProcessingStatus], n: int) -> List[int]:
    db_processing_statuses = (
        db.query(model)
        .filter(model.status == models.ProcessingStatusType.not_processed)
        .order_by(model.created_at)
        .limit(n)
    )
    source_text_ids = [db_processing_status.source_text_id for db_processing_status in db_processing_statuses]
    return source_text_ids
