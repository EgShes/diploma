from typing import Optional, List

import sqlalchemy
from fastapi import FastAPI, HTTPException
from fastapi.params import Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from config import DbConfig


class TextBase(SQLModel):
    raw_text: Optional[str]
    source: Optional[str]


class Text(TextBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class TextCreate(TextBase):
    pass


class TextRead(TextBase):
    id: int


engine = create_engine(DbConfig.get_db_url())


def create_db_and_tables():
    while True:
        try:
            SQLModel.metadata.create_all(engine)
            break
        except sqlalchemy.exc.OperationalError:
            pass


def create_texts():
    text_1 = Text(raw_text="Привет. Ты сделала отчет?", source="Telegram")
    text_2 = Text(raw_text="А то сроки горят", source="Telegram")
    text_3 = Text(raw_text="Срочно нужен сегодня к трем", source="Telegram")

    with Session(engine) as session:
        session.add(text_1)
        session.add(text_2)
        session.add(text_3)

        session.commit()


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


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
