from fastapi import APIRouter

from app.core.deps import DB, CurrentUser
from app.schemas.vehicle import VehicleOut
from app.services import transfers as svc

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])


@router.get("/search", response_model=list[VehicleOut])
def search_vehicles(q: str, _: CurrentUser, db: DB):
    """Search saved vehicles by registration, chassis or engine number (min 2 characters)."""
    return svc.search_vehicles(db, q)
