from typing import Type

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
