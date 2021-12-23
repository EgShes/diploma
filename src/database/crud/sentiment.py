from sqlalchemy.orm import Session

from src.database import models, schemas
from src.database.crud.processing_status import update_processing_status


def create_sentiment(db: Session, source_text_id: int, sentiment: schemas.SentimentCreate) -> models.Sentiment:
    db_sentiment = models.Sentiment(
        type=sentiment.type, probability=sentiment.probability, source_text_id=source_text_id
    )
    db.add(db_sentiment)
    db.commit()
    db.refresh(db_sentiment)
    update_processing_status(
        db, models.SentimentProcessingStatus, source_text_id, models.ProcessingStatusType.processed
    )
    return db_sentiment
