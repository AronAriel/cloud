from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Feedback(Base):
    __tablename__ = "feedbacks"
    __table_args__ = {"schema": "feedback"}

    id = Column(Integer, primary_key=True)
    consultation_id = Column(Integer)
    rating = Column(Integer)
    comment = Column(String)