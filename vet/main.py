from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from db import SessionLocal
from services import list_vets
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()


@strawberry.type
class VetType:
    id: int
    name: str
    specialization: str


@strawberry.type
class Query:
    @strawberry.field
    def vets(self) -> list[VetType]:
        return get_vets()


def get_vets():
    logger.info("Fetching vets")

    db = SessionLocal()

    try:
        vets = [
            VetType(
                id=vet["id"],
                name=vet["name"],
                specialization=vet["specialization"],
            )
            for vet in list_vets(db)
        ]
        logger.info(f"Found {len(vets)} vets")
        return vets

    except Exception as e:
        logger.error(f"Error fetching vets: {e}")
        raise
    finally:
        if hasattr(db, "close"):
            db.close()


schema = strawberry.Schema(query=Query)
app.include_router(GraphQLRouter(schema), prefix="/graphql")


@app.on_event("startup")
def startup():
    logger.info("Vet Service started")
