from pydantic import BaseModel, Field
from typing import Optional, List


class DepartmentBase(BaseModel):
    num_departement: int
    nom_departement: str


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    num_departement: Optional[int] = None
    nom_departement: Optional[str] = None

    class Config:
        orm_mode = True


class DepartmentRead(DepartmentBase):
    id: int

    class Config:
        orm_mode = True


class IndicateurBase(BaseModel):
    source: str
    type: str
    value: float
    unit: str
    year: int


class IndicateurCreate(IndicateurBase):
    departement_id: int


class IndicateurUpdate(BaseModel):
    source: Optional[str] = None
    type: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    year: Optional[int] = None

    class Config:
        orm_mode = True


class IndicateurRead(IndicateurBase):
    id: int
    departement_id: int

    class Config:
        orm_mode = True
