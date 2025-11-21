from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from models import Department, Indicateur
from schemas import DepartmentCreate, DepartmentRead, IndicateurCreate, IndicateurRead
from database import get_db


def get_departments(session: Session, skip: int = 0, limit: int = 100):
    departments = session.query(Department).offset(skip).limit(limit).all()
    return departments
