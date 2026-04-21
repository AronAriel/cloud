from sqlalchemy import Column, Integer, String
from db import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Vet(Base):
    __tablename__ = "vets"
    __table_args__ = {"schema": "vet"}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    specialization = Column(String) 