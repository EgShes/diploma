from typing import List

from sqlalchemy.orm import Session

from src.database import models, schemas
from src.database.crud.common import get_by_id_list
from src.database.crud.processing_status import (
    get_oldest_not_processed,
    update_processing_status,
)


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


def get_sentiment_by_ids(db: Session, ids: List[int]) -> List[schemas.Sentiment]:
    return get_by_id_list(db, models.Sentiment, ids)


def get_oldest_not_processed_sentiments(db: Session, n: int) -> List[int]:
    source_text_ids = get_oldest_not_processed(db, models.SentimentProcessingStatus, n)
    update_processing_status(
        db, models.SentimentProcessingStatus, source_text_ids, models.ProcessingStatusType.processing
    )
    return source_text_ids
