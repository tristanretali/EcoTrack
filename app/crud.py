from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List
from models import Department, Indicateur
from schemas import (
    DepartmentCreate,
    DepartmentRead,
    IndicateurCreate,
    IndicateurRead,
    DepartmentUpdate,
    IndicateurUpdate,
)
from database import get_db
from sqlalchemy.exc import IntegrityError


def get_departments(
    session: Session,
    skip: int = 0,
    limit: int = 10,
    search: str = None,
):

    query = session.query(Department).options(joinedload(Department.indicateurs))

    if search:
        query = query.filter(Department.nom_departement.ilike(f"%{search}%"))

    departments = query.offset(skip).limit(limit).all()

    return departments


def get_department(id: int, session: Session):
    department = (
        session.query(Department).options(joinedload(Department.indicateurs)).get(id)
    )
    if not department:
        raise HTTPException(status_code=404, detail="Département non trouvé")
    return department


def create_department(session: Session, department_data: DepartmentCreate):
    department = Department(**department_data.model_dump())
    try:
        session.add(department)
        session.commit()
        return department_data.model_dump()

    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Conflit : Un département avec le même nom ou numéro existe déjà",
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Une erreur inattendue est survenue: {str(e)}"
        )


def update_department(
    id: int, department_data: DepartmentUpdate, session: Session = Depends(get_db)
):
    department = session.query(Department).get(id)
    if not department:
        raise HTTPException(status_code=404, detail="Département non trouvé")

    for key, value in department_data.model_dump().items():
        if value is not None:
            setattr(department, key, value)

    session.commit()
    session.refresh(department)

    return department


def get_indicateurs(
    session: Session, skip: int = 0, limit: int = 10, type: str = None, year: int = None
):
    query = session.query(Indicateur).options(joinedload(Indicateur.department))

    if type:
        query = query.filter(Indicateur.type == type)

    if year:
        query = query.filter(Indicateur.year == year)

    indicateurs = query.offset(skip).limit(limit).all()

    return indicateurs


def get_indicateur(id: int, session: Session):
    indicateur = (
        session.query(Indicateur).options(joinedload(Indicateur.department)).get(id)
    )
    if not indicateur:
        raise HTTPException(status_code=404, detail="Indicateur non trouvé")
    return indicateur


def create_indicateur(session: Session, indicateur_data: IndicateurCreate):
    department = session.query(Department).get(indicateur_data.departement_id)
    print(department)
    if not department:
        raise HTTPException(status_code=404, detail="Département non trouvé")
    indicateur = Indicateur(**indicateur_data.model_dump())

    try:
        session.add(indicateur)
        session.commit()
        return indicateur_data.model_dump()

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Une erreur inattendue est survenue: {str(e)}"
        )


def update_indicateur(
    id: int, indicator_data: IndicateurUpdate, db: Session = Depends(get_db)
):
    indicateur = db.query(Indicateur).get(id)
    if not indicateur:
        raise HTTPException(status_code=404, detail="Indicateur non trouvé")

    for key, value in indicator_data.model_dump().items():
        if value is not None:
            setattr(indicateur, key, value)

    db.commit()
    db.refresh(indicateur)

    return indicateur
