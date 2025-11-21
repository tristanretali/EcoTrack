from pydantic import BaseModel, Field
from typing import Optional, List


class DepartmentCreate(BaseModel):
    num_departement: int
    nom_departement: str


class DepartmentUpdate(BaseModel):
    num_departement: Optional[int] = None
    nom_departement: Optional[str] = None

    class Config:
        orm_mode = True


class IndicateurCreate(BaseModel):
    source: str
    type: str
    value: float
    unit: str
    year: int
    departement_id: int


class IndicateurUpdate(BaseModel):
    source: Optional[str] = None
    type: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    year: Optional[int] = None

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    email: str = Field(description="Adresse e-mail de l'utilisateur")
    password: str = Field(description="Mot de passe de l'utilisateur", min_length=3)

    class Config:
        orm_mode = True
