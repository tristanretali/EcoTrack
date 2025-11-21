from fastapi import HTTPException, Depends
from security import verify_password, hash_password
from sqlalchemy.orm import Session, joinedload
from typing import List
from models import Department, Indicateur, User
from schemas import (
    DepartmentCreate,
    IndicateurCreate,
    DepartmentUpdate,
    IndicateurUpdate,
    UserSchema,
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


def delete_department(id: int, session: Session = Depends(get_db)):
    department = session.query(Department).get(id)
    if not department:
        raise HTTPException(status_code=404, detail="Département non trouvé")

    session.delete(department)
    session.commit()


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


def update_indicateur(id: int, indicator_data: IndicateurUpdate, session: Session):
    indicateur = session.query(Indicateur).get(id)
    if not indicateur:
        raise HTTPException(status_code=404, detail="Indicateur non trouvé")

    for key, value in indicator_data.model_dump().items():
        if value is not None:
            setattr(indicateur, key, value)

    session.commit()
    session.refresh(indicateur)

    return indicateur


def delete_indicateur(id: int, session: Session):
    indicateur = session.query(Indicateur).get(id)

    if not indicateur:
        raise HTTPException(status_code=404, detail="Indicateur non trouvé")

    session.delete(indicateur)
    session.commit()


def create_user(session: Session, user_data: UserSchema):
    hashed_pw = hash_password(user_data.password)

    user = User(
        email=user_data.email,
        password=hashed_pw,
    )

    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Conflit : Un utilisateur avec le même mail existe déjà",
        )


def login_user(session: Session, user_data: UserSchema):
    user = session.query(User).filter(User.email == user_data.email).first()
    print(user)
    if user and verify_password(user_data.password, user.password):
        return user
    raise HTTPException(
        status_code=500,
        detail="invalid_credentials",
    )


def get_user_by_id(session: Session, user_id: int):
    return session.query(User).filter(User.id == user_id).first()


def get_users(session: Session, skip: int = 0, limit: int = 10):
    return session.query(User).offset(skip).limit(limit).all()


def delete_user(id: int, session: Session):
    user = session.query(User).get(id)

    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    session.delete(user)
    session.commit()


def change_user_role(id: int, new_role: str, session: Session):
    user = session.query(User).get(id)

    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    user.role = new_role
    session.commit()
    session.refresh(user)

    return user
