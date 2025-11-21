from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    UniqueConstraint,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    num_departement = Column(Integer, unique=True, nullable=False)
    nom_departement = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("num_departement", "nom_departement", name="uq_department"),
    )


class Indicateur(Base):
    __tablename__ = "indicateurs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String, nullable=False)
    type = Column(String, nullable=False)
    departement_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    year = Column(Integer, nullable=True)


Department.indicateurs = relationship(
    "Indicateur", back_populates="department", cascade="all, delete"
)
Indicateur.department = relationship("Department", back_populates="indicateurs")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")

    __table_args__ = (UniqueConstraint("email", name="uq_email"),)
