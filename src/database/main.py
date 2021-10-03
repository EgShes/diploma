from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.params import Query
from sqlmodel import Session, create_engine, select

from config import DbConfig
from src.database.models import TextRead, TextCreate, Text
from src.database.utils import create_db_and_tables

engine = create_engine(DbConfig.get_db_url())


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables(engine)


@app.post("/add_text/", response_model=TextRead)
def add_text(text: TextCreate):
    with Session(engine) as session:
        db_text = Text.from_orm(text)
        session.add(db_text)
        session.commit()
        session.refresh(db_text)
        return db_text


@app.get("/texts/", response_model=List[TextRead])
def texts(offset: int = 0, limit: int = Query(default=100, lte=100)):
    with Session(engine) as session:
        texts = session.exec(select(Text).offset(offset).limit(limit)).all()
        return texts


@app.get("/text/{text_id}", response_model=TextRead)
def read_text(text_id: int):
    with Session(engine) as session:
        text = session.get(Text, text_id)
        if not text:
            raise HTTPException(status_code=404, detail="Text not found")
        return text
