from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query
from pydantic import conlist
from sqlalchemy.orm import Session

from src.database import schemas
from src.database.crud.exceptions import NotExistsError
from src.database.crud.text import create_source_text, get_source_text_by_ids
from src.database.routers.utils import get_db

router = APIRouter()


@router.post("/add/", response_model=schemas.SourceText)
def add_text(text: schemas.SourceTextCreate, db: Session = Depends(get_db)) -> schemas.SourceText:
    try:
        source_text_db = create_source_text(db=db, source_text=text)
    except NotExistsError as e:
        raise HTTPException(404, detail=e.args[0])
    return source_text_db


@router.get("/read/", response_model=List[schemas.SourceText])
def get_texts(ids: conlist(int, max_items=50) = Query(...), db: Session = Depends(get_db)) -> List[schemas.SourceText]:
    return get_source_text_by_ids(db, ids)
