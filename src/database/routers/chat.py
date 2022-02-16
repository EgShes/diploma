from typing import List

from fastapi import APIRouter
from fastapi.params import Depends, Query
from pydantic import conint, conlist
from sqlalchemy.orm import Session

from src.database import schemas
from src.database.crud.chat import create_chat, get_chat_by_ids
from src.database.routers.utils import get_db

router = APIRouter()


@router.post("/add/", response_model=schemas.Chat)
def add_chat(chat: schemas.ChatCreate, db: Session = Depends(get_db)) -> schemas.Chat:
    chat_db = create_chat(db, chat=chat)
    return chat_db


@router.get("/read/", response_model=List[schemas.Chat])
def get_chats(
    ids: conlist(conint(gt=0), max_items=50) = Query(...), db: Session = Depends(get_db)
) -> List[schemas.Chat]:
    return get_chat_by_ids(db, ids)
