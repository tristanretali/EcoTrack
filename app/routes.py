from crud import (
    get_departments,
    get_department,
    get_indicateurs,
    get_indicateur,
    create_department,
    create_indicateur,
    update_department,
    update_indicateur,
)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import (
    DepartmentCreate,
    IndicateurCreate,
    DepartmentUpdate,
    IndicateurUpdate,
)


router = APIRouter()


@router.get("/departments/")
def read_departments(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db), search: str = None
):
    departments = get_departments(db, skip, limit, search)

    return departments


@router.get("/department/{id}")
def read_department(id: int, db: Session = Depends(get_db)):
    department = get_department(id, db)

    return department


@router.post("/department/create")
def create_new_department(
    department_data: DepartmentCreate, db: Session = Depends(get_db)
):
    department = create_department(db, department_data)

    return department


@router.post("/department/update/{id}")
def update_existing_department(
    id: int, department_data: DepartmentUpdate, db: Session = Depends(get_db)
):
    department = update_department(id, department_data, db)

    return department


@router.get("/indicateurs/")
def read_indicateurs(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    type: str = None,
    year: int = None,
):
    indicateurs = get_indicateurs(db, skip, limit, type, year)

    return indicateurs


@router.get("/indicateur/{id}")
def read_indicateur(id: int, db: Session = Depends(get_db)):
    indicateur = get_indicateur(id, db)

    return indicateur


@router.post("/indicateur/create")
def create_new_indicateur(
    indicator_data: IndicateurCreate, db: Session = Depends(get_db)
):
    indicateur = create_indicateur(db, indicator_data)

    return indicateur


@router.post("/indicateur/update/{id}")
def update_existing_indicateur(
    id: int, indicator_data: IndicateurUpdate, db: Session = Depends(get_db)
):
    indicateur = update_indicateur(id, indicator_data, db)

    return indicateur
