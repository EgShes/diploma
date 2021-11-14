from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.config import dev_logger
from src.database import models, schemas


class AlreadyExistsError(Exception):
    pass


# source text


def get_source_text(db: Session, id_: int):
    return db.query(models.SourceText).filter(models.SourceText.id == id_).first()


def create_source_text(db: Session, source_text: schemas.SourceTextCreate) -> models.SourceText:
    db_source_text = models.SourceText(text=source_text.text, source=source_text.source)
    db.add(db_source_text)
    db.commit()
    db.refresh(db_source_text)
    return db_source_text


def get_texts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SourceText).offset(skip).limit(limit).all()


# named entity


def create_named_entity(
    db: Session, source_text_id: int, named_entity: schemas.NamedEntityCreate
) -> models.NamedEntity:
    db_named_entity = models.NamedEntity(text=named_entity.text, type=named_entity.type, source_text_id=source_text_id)
    db.add(db_named_entity)
    db.commit()
    db.refresh(db_named_entity)
    return db_named_entity


# word


def create_word(db: Session, source_text_id: int, word: schemas.WordCreate) -> models.SourceTextWordAssociation:
    source_text = db.query(models.SourceText).filter(models.SourceText.id == source_text_id).first()
    association = models.SourceTextWordAssociation(quantity=word.quantity)
    association.word = db.query(models.Word).filter(models.Word.text == word.text).first() or models.Word(
        text=word.text
    )
    source_text.words.append(association)
    db.add(association)
    try:
        db.commit()
        db.refresh(association)
    except IntegrityError as e:
        raise AlreadyExistsError("Data you are trying to insert already exists") from e
    dev_logger.debug("Successfully added a word")
    return association
