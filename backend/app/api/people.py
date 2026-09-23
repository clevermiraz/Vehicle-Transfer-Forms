from fastapi import APIRouter

from app.core.deps import DB, CurrentUser
from app.schemas.person import PersonOut
from app.services import transfers as svc

router = APIRouter(prefix="/api/people", tags=["people"])


@router.get("/search", response_model=list[PersonOut])
def search_people(q: str, _: CurrentUser, db: DB):
    """Search saved customers by name, NID or mobile (min 2 characters)."""
    return svc.search_people(db, q)
