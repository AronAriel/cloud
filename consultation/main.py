from fastapi import FastAPI
from db import SessionLocal
from models import Consultation

app = FastAPI()

@app.get("/consultations")
def get_consultations():
    db = SessionLocal()
    consultations = db.query(Consultation).all()

    return [
        {
            "id": c.id,
            "pet_name": c.pet_name,
            "date": str(c.date),
            "vet_id": c.vet_id
        }
        for c in consultations
    ]