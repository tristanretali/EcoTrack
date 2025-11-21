from crud import get_departments
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter()


@router.get("/departments/")
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    departments = get_departments(db, skip=skip, limit=limit)
    return departments
