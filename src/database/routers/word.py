from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query
from pydantic import conlist
from sqlalchemy.orm import Session

from src.database import schemas
from src.database.crud.exceptions import AlreadyExistsError
from src.database.crud.text import get_source_text_by_id, get_source_text_by_ids
from src.database.crud.word import (
    create_word,
    get_oldest_not_processed_words,
    get_word_by_ids,
)
from src.database.routers.utils import get_db

router = APIRouter()


@router.post("/add/", response_model=schemas.Word)
def create_word_for_text(text_id: int, word: schemas.WordCreate, db: Session = Depends(get_db)):
    source_text = get_source_text_by_id(db, id_=text_id)
    if source_text is None:
        raise HTTPException(status_code=404, detail=f"Text with id {text_id} not found")
    try:
        association = create_word(db, source_text_id=text_id, word=word)
    except AlreadyExistsError as e:
        raise HTTPException(403, detail=e.args)
    association.word.source_text_id = association.source_text_id
    return schemas.Word.from_orm(association.word)


@router.get("/for_processing/", response_model=List[schemas.SourceText])
def get_source_texts_for_processing(n: int, db: Session = Depends(get_db)) -> List[schemas.SourceText]:
    source_text_ids = get_oldest_not_processed_words(db, n)
    if not source_text_ids:
        return []
    return get_source_text_by_ids(db, source_text_ids)


@router.get("/read/", response_model=List[schemas.Word])
def get_words(ids: conlist(int, max_items=50) = Query(...), db: Session = Depends(get_db)) -> List[schemas.Word]:
    return get_word_by_ids(db, ids)
