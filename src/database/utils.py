import sqlalchemy
from sqlmodel import SQLModel


def create_db_and_tables(engine):
    while True:
        try:
            SQLModel.metadata.create_all(engine)
            break
        except sqlalchemy.exc.OperationalError:
            pass
