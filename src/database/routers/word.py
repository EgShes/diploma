from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query
from pydantic import conint, conlist
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
    # TODO fix assisiation between word and text
    association.word.source_text_ids = [association.source_text_id]
    return schemas.Word.from_orm(association.word)


@router.get("/for_processing/", response_model=List[schemas.SourceText])
def get_source_texts_for_processing(n: conint(gt=0), db: Session = Depends(get_db)) -> List[schemas.SourceText]:
    source_text_ids = get_oldest_not_processed_words(db, n)
    if not source_text_ids:
        raise HTTPException(status_code=404, detail="No data for processing")
    return get_source_text_by_ids(db, source_text_ids)


@router.get("/read/", response_model=List[schemas.Word])
def get_words(ids: conlist(int, max_items=50) = Query(...), db: Session = Depends(get_db)) -> List[schemas.Word]:
    return_words = []
    for word in get_word_by_ids(db, ids):
        return_words.append(
            schemas.Word(
                id=word.id,
                text=word.text,
                created_at=word.created_at,
                source_text_ids=[source_text_word.source_text_id for source_text_word in word.source_texts],
            )
        )
    return return_words
