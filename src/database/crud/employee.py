from typing import List

from sqlalchemy.orm import Session

from src.database import models, schemas
from src.database.crud.common import get_by_id, get_by_id_list


def get_employee_by_id(db: Session, id_: int) -> schemas.Employee:
    return get_by_id(db, models.Employee, id_)


def get_employee_by_ids(db: Session, ids: List[int]) -> List[schemas.Employee]:
    return get_by_id_list(db, models.Employee, ids)


def create_employee(db: Session, employee: schemas.EmployeeCreate) -> models.Employee:
    employee = models.Employee(
        passport=employee.passport,
        first_name=employee.first_name,
        second_name=employee.second_name,
        third_name=employee.third_name,
        department=employee.department,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee
