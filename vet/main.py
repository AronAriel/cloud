from fastapi import FastAPI
from db import SessionLocal
from services import list_vets
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
        vets = list_vets(db)
        logger.info(f"Found {len(vets)} vets")
        return vets

    except Exception as e:
        logger.error(f"Error fetching vets: {e}")
        raise
    finally:
        if hasattr(db, "close"):
            db.close()


@app.on_event("startup")
def startup():
    logger.info("Vet Service started")
