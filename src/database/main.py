from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.database import crud, models, schemas
from src.database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/add_text/", response_model=schemas.SourceText)
def add_text(text: schemas.SourceTextCreate, db: Session = Depends(get_db)):
    return crud.create_source_text(db=db, source_text=text)


@app.get("/text/", response_model=schemas.SourceText)
def read_text(text_id: int, db: Session = Depends(get_db)):
    source_text = crud.get_source_text(db, id_=text_id)
    if source_text is None:
        raise HTTPException(status_code=404, detail="Text not found")
    return source_text


@app.get("/texts/", response_model=List[schemas.SourceText])
def read_texts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_texts(db, skip=skip, limit=limit)


@app.post("/named_entity", response_model=schemas.NamedEntity)
def create_named_entity_for_text(text_id: int, named_entity: schemas.NamedEntityCreate, db: Session = Depends(get_db)):
    return crud.create_named_entity(db, source_text_id=text_id, named_entity=named_entity)
