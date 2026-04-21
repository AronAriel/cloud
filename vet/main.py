from fastapi import FastAPI
from db import SessionLocal
from models import Vet

app = FastAPI()

@app.get("/vets")
def get_vets():
    db = SessionLocal()
    vets = db.query(Vet).all()
    
    return [
        {
            "id": v.id,
            "name": v.name,
            "specialization": v.specialization
        }
        for v in vets
    ]