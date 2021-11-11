from sqlalchemy.orm import Session

from src.database import models, schemas


def get_source_text(db: Session, id_: int):
    return db.query(models.SourceText).filter(models.SourceText.id == id_).first()


def create_source_text(db: Session, source_text: schemas.SourceTextCreate):
    db_source_text = models.SourceText(text=source_text.text, source=source_text.source)
    db.add(db_source_text)
    db.commit()
    db.refresh(db_source_text)
    return db_source_text


def get_texts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SourceText).offset(skip).limit(limit).all()
