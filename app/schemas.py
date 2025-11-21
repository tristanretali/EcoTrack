from pydantic import BaseModel, Field
from typing import Optional, List


class DepartmentBase(BaseModel):
    num_departement: int
    nom_departement: str


class DepartmentCreate(DepartmentBase):
    pass


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


class IndicateurRead(IndicateurBase):
    id: int
    departement_id: int

    class Config:
        orm_mode = True
