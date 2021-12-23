from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.database import crud, schemas
from src.database.routers.utils import get_db

router = APIRouter()


@router.post("/add/", response_model=schemas.Sentiment)
def create_sentiment_for_text(text_id: int, sentiment: schemas.SentimentCreate, db: Session = Depends(get_db)):
    return crud.create_sentiment(db, source_text_id=text_id, sentiment=sentiment)
