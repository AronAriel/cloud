from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Consultation(Base):
    __tablename__ = "consultations"
    __table_args__ = {"schema": "consultation"}

    id = Column(Integer, primary_key=True)
    pet_name = Column(String)
    date = Column(DateTime)
    vet_id = Column(Integer)