from typing import List

from fastapi import APIRouter
from fastapi.params import Depends, Query
from pydantic import conint, conlist
from sqlalchemy.orm import Session

from src.database import schemas
from src.database.crud.employee import create_employee, get_employee_by_ids
from src.database.routers.utils import get_db

router = APIRouter()


@router.post("/add/", response_model=schemas.Employee)
def add_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)) -> schemas.Employee:
    employee_db = create_employee(db, employee=employee)
    return employee_db


@router.get("/read/", response_model=List[schemas.Employee])
def get_employees(
    ids: conlist(conint(gt=0), max_items=50) = Query(...), db: Session = Depends(get_db)
) -> List[schemas.SourceText]:
    return get_employee_by_ids(db, ids)
