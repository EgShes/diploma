from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.database import crud, schemas
from src.database.routers.utils import get_db

router = APIRouter()


@router.post("/add/", response_model=schemas.NamedEntity)
def create_named_entity_for_text(text_id: int, named_entity: schemas.NamedEntityCreate, db: Session = Depends(get_db)):
    return crud.create_named_entity(db, source_text_id=text_id, named_entity=named_entity)
