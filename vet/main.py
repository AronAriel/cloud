from fastapi import FastAPI
from db import SessionLocal
from models import Vet
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/vets")
def get_vets():
    logger.info("Fetching vets")

    db = SessionLocal()

    try:
        vets = db.query(Vet).all()
        logger.info(f"Found {len(vets)} vets")

        return [
            {
                "id": v.id,
                "name": v.name,
                "specialization": v.specialization
            }
            for v in vets
        ]

    except Exception as e:
        logger.error(f"Error fetching vets: {e}")
        raise


@app.on_event("startup")
def startup():
    logger.info("Vet Service started")