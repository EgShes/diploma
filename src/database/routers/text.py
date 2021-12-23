from typing import List

from fastapi import APIRouter
from fastapi.params import Depends, Query
from pydantic import conlist
from sqlalchemy.orm import Session

from src.database import schemas
from src.database.crud.text import create_source_text, get_source_text_by_ids
from src.database.routers.utils import get_db

router = APIRouter()


@router.post("/add/", response_model=schemas.SourceText)
def add_text(text: schemas.SourceTextCreate, db: Session = Depends(get_db)) -> schemas.SourceText:
    return create_source_text(db=db, source_text=text)


@router.get("/read/", response_model=List[schemas.SourceText])
def get_texts(ids: conlist(int, max_items=50) = Query(...), db: Session = Depends(get_db)) -> List[schemas.SourceText]:
    return get_source_text_by_ids(db, ids)
