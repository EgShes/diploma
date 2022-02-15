from fastapi import FastAPI

from src.database import models
from src.database.database import engine
from src.database.routers import (
    employee,
    health_check,
    named_entity,
    sentiment,
    text,
    word,
)

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(text.router, prefix="/text", tags=["text"])
app.include_router(employee.router, prefix="/employee", tags=["employee"])
app.include_router(word.router, prefix="/word", tags=["word"])
app.include_router(named_entity.router, prefix="/named_entity", tags=["named_entity"])
app.include_router(sentiment.router, prefix="/sentiment", tags=["sentiment"])
app.include_router(health_check.router, tags=["checks"])
