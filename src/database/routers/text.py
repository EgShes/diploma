from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.database import crud, schemas
from src.database.routers.utils import get_db

router = APIRouter()


@router.post("/add/", response_model=schemas.SourceText)
def add_text(text: schemas.SourceTextCreate, db: Session = Depends(get_db)):
    return crud.create_source_text(db=db, source_text=text)


@router.get("/read/", response_model=schemas.SourceText)
def read_text(text_id: int, db: Session = Depends(get_db)):
    source_text = crud.get_source_text(db, id_=text_id)
    if source_text is None:
        raise HTTPException(status_code=404, detail=f"Text with id {text_id} not found")
    return source_text


@router.get("/list/", response_model=List[schemas.SourceText])
def read_texts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_texts(db, skip=skip, limit=limit)
