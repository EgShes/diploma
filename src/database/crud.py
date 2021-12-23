from typing import Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import models, schemas


class AlreadyExistsError(Exception):
    pass


# processing status


def create_processing_status(db: Session, id_: int):
    for Model in [models.WordProcessingStatus, models.NamedEntityProcessingStatus, models.SentimentProcessingStatus]:
        db_processing_status = Model(status=models.ProcessingStatusType.not_processed, source_text_id=id_)
        db.add(db_processing_status)
    db.commit()


def update_processing_status(
    db: Session, model: Type[models.ProcessingStatus], id_: int, status: models.ProcessingStatusType
):
    db_processing_status = db.query(model).filter(model.source_text_id == id_).first()
    db_processing_status.status = status
    db.commit()


# source text


def get_source_text(db: Session, id_: int):
    return db.query(models.SourceText).filter(models.SourceText.id == id_).first()


def create_source_text(db: Session, source_text: schemas.SourceTextCreate) -> models.SourceText:
    db_source_text = models.SourceText(text=source_text.text, source=source_text.source)
    db.add(db_source_text)
    db.commit()
    db.refresh(db_source_text)
    create_processing_status(db, db_source_text.id)
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
    update_processing_status(
        db, models.NamedEntityProcessingStatus, source_text_id, models.ProcessingStatusType.processed
    )
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
    update_processing_status(db, models.WordProcessingStatus, source_text_id, models.ProcessingStatusType.processed)
    return association


# sentiment


def create_sentiment(db: Session, source_text_id: int, sentiment: schemas.SentimentCreate) -> models.Sentiment:
    db_sentiment = models.Sentiment(
        type=sentiment.type, probability=sentiment.probability, source_text_id=source_text_id
    )
    db.add(db_sentiment)
    db.commit()
    db.refresh(db_sentiment)
    update_processing_status(
        db, models.SentimentProcessingStatus, source_text_id, models.ProcessingStatusType.processed
    )
    return db_sentiment
