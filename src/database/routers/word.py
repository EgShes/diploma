from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.database import schemas
from src.database.crud.exceptions import AlreadyExistsError
from src.database.crud.text import get_source_text
from src.database.crud.word import create_word
from src.database.routers.utils import get_db

router = APIRouter()


@router.post("/add/", response_model=schemas.Word)
def create_word_for_text(text_id: int, word: schemas.WordCreate, db: Session = Depends(get_db)):
    source_text = get_source_text(db, id_=text_id)
    if source_text is None:
        raise HTTPException(status_code=404, detail=f"Text with id {text_id} not found")
    try:
        association = create_word(db, source_text_id=text_id, word=word)
    except AlreadyExistsError as e:
        raise HTTPException(403, detail=e.args)
    association.word.source_text_id = association.source_text_id
    return schemas.Word.from_orm(association.word)
