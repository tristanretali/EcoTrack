from crud import get_departments, get_department, get_indicateurs, get_indicateur
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter()


@router.get("/departments/")
def read_departments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    departments = get_departments(db, skip=skip, limit=limit)

    return departments


@router.get("/department/{id}")
def read_department(id: int, db: Session = Depends(get_db)):
    department = get_department(id, db)

    return department


@router.get("/indicateurs/")
def read_indicateurs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    indicateurs = get_indicateurs(db, skip=skip, limit=limit)

    return indicateurs


@router.get("/indicateur/{id}")
def read_indicateur(id: int, db: Session = Depends(get_db)):
    indicateur = get_indicateur(id, db)

    return indicateur
