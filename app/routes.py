from crud import (
    get_departments,
    get_department,
    get_indicateurs,
    get_indicateur,
    create_department,
    create_indicateur,
    update_department,
    update_indicateur,
    create_user,
    login_user,
    delete_department,
    delete_indicateur,
)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import (
    DepartmentCreate,
    IndicateurCreate,
    DepartmentUpdate,
    IndicateurUpdate,
    UserSchema,
)
from auth import (
    timedelta,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
)


router = APIRouter()


@router.get("/departments/")
def read_departments(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    search: str = None,
):
    departments = get_departments(db, skip, limit, search)

    return departments


@router.get("/department/{id}")
def read_department(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    department = get_department(id, db)

    return department


@router.post("/department/create")
def create_new_department(
    department_data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Accès refusé : seul un administrateur peut modifier un film.",
        )
    department = create_department(db, department_data)

    return department


@router.post("/department/update/{id}")
def update_existing_department(
    id: int,
    department_data: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Accès refusé : seul un administrateur peut modifier un film.",
        )
    department = update_department(id, department_data, db)

    return department


@router.delete("/department/delete/{id}")
def delete_existing_department(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Accès refusé : seul un administrateur peut modifier un film.",
        )
    delete_department(id, db)


@router.get("/indicateurs/")
def read_indicateurs(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    type: str = None,
    year: int = None,
):
    indicateurs = get_indicateurs(db, skip, limit, type, year)

    return indicateurs


@router.get("/indicateur/{id}")
def read_indicateur(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    indicateur = get_indicateur(id, db)

    return indicateur


@router.post("/indicateur/create")
def create_new_indicateur(
    indicator_data: IndicateurCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Accès refusé : seul un administrateur peut modifier un film.",
        )
    indicateur = create_indicateur(db, indicator_data)

    return indicateur


@router.post("/indicateur/update/{id}")
def update_existing_indicateur(
    id: int,
    indicator_data: IndicateurUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Accès refusé : seul un administrateur peut modifier un film.",
        )
    indicateur = update_indicateur(id, indicator_data, db)

    return indicateur


@router.delete("/indicateur/delete/{id}")
def delete_existing_indicateur(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Accès refusé : seul un administrateur peut modifier un film.",
        )

    delete_indicateur(id, db)


@router.post("/register")
def create_new_user(user_data: UserSchema, db: Session = Depends(get_db)):
    user = create_user(db, user_data)

    return user


@router.post("/login", status_code=201)
def login(user_data: UserSchema, db: Session = Depends(get_db)):
    user = login_user(db, user_data)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
