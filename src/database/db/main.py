from typing import Optional


import sqlalchemy
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from config import DbConfig


class Text(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    raw_text: Optional[str]
    source: Optional[str]


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
    create_texts()


@app.get("/texts/")
def read_texts():
    with Session(engine) as session:
        texts = session.exec(select(Text)).all()
        return texts
