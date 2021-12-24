from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import models, schemas
from src.database.crud.common import get_by_id_list
from src.database.crud.exceptions import AlreadyExistsError
from src.database.crud.processing_status import (
    get_oldest_not_processed,
    update_processing_status,
)


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


def get_word_by_ids(db: Session, ids: List[int]) -> List[schemas.Word]:
    return get_by_id_list(db, models.Word, ids)


def get_oldest_not_processed_words(db: Session, n: int) -> List[int]:
    source_text_ids = get_oldest_not_processed(db, models.WordProcessingStatus, n)
    update_processing_status(db, models.WordProcessingStatus, source_text_ids, models.ProcessingStatusType.processing)
    return source_text_ids
