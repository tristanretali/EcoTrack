from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List
from models import Department, Indicateur
from schemas import DepartmentCreate, DepartmentRead, IndicateurCreate, IndicateurRead
from database import get_db


def get_departments(session: Session, skip: int = 0, limit: int = 10):
    departments = (
        session.query(Department)
        .options(joinedload(Department.indicateurs))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return departments


def get_department(id: int, session: Session):
    department = (
        session.query(Department).options(joinedload(Department.indicateurs)).get(id)
    )
    if not department:
        raise HTTPException(status_code=404, detail="Département non trouvé")
    return department


def get_indicateurs(session: Session, skip: int = 0, limit: int = 10):
    indicateurs = (
        session.query(Indicateur)
        .options(joinedload(Indicateur.department))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return indicateurs


def get_indicateur(id: int, session: Session):
    indicateur = (
        session.query(Indicateur).options(joinedload(Indicateur.department)).get(id)
    )
    if not indicateur:
        raise HTTPException(status_code=404, detail="Indicateur non trouvé")
    return indicateur
