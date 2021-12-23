from typing import List

from fastapi import APIRouter
from fastapi.params import Depends, Query
from pydantic import conlist
from sqlalchemy.orm import Session

from src.database import schemas
from src.database.crud.sentiment import (
    create_sentiment,
    get_oldest_not_processed_sentiments,
    get_sentiment_by_ids,
)
from src.database.crud.text import get_source_text_by_ids
from src.database.routers.utils import get_db

router = APIRouter()


@router.post("/add/", response_model=schemas.Sentiment)
def create_sentiment_for_text(text_id: int, sentiment: schemas.SentimentCreate, db: Session = Depends(get_db)):
    return create_sentiment(db, source_text_id=text_id, sentiment=sentiment)


@router.get("/for_processing/", response_model=List[schemas.SourceText])
def get_source_texts_for_processing(n: int, db: Session = Depends(get_db)) -> List[schemas.SourceText]:
    source_text_ids = get_oldest_not_processed_sentiments(db, n)
    if not source_text_ids:
        return []
    return get_source_text_by_ids(db, source_text_ids)


@router.get("/read/", response_model=List[schemas.Sentiment])
def get_sentiments(
    ids: conlist(int, max_items=50) = Query(...), db: Session = Depends(get_db)
) -> List[schemas.Sentiment]:
    return get_sentiment_by_ids(db, ids)
