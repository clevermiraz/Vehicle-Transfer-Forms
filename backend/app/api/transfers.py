from fastapi import APIRouter, status

from app.core.deps import DB, CurrentUser
from app.schemas.transfer import TransferDefaults, TransferIn, TransferListItem, TransferOut
from app.services import transfers as svc
from app.services.money import amount_in_words, format_taka

router = APIRouter(prefix="/api/transfers", tags=["transfers"])


@router.get("", response_model=list[TransferListItem])
def list_transfers(_: CurrentUser, db: DB, q: str | None = None):
    """Latest transfers, or search by registration number, NID, mobile, seller or buyer name."""
    return [svc.list_item(t) for t in svc.search_transfers(db, q)]


@router.get("/defaults", response_model=TransferDefaults)
def defaults(_: CurrentUser, db: DB):
    """Values pre-filled on a new transfer (last used registration authority and bank)."""
    return svc.last_used_defaults(db)


@router.get("/amount-in-words")
def amount_words(amount: int, _: CurrentUser):
    return {"figures": format_taka(amount), "words": amount_in_words(amount)}


@router.post("", response_model=TransferOut, status_code=status.HTTP_201_CREATED)
def create_transfer(data: TransferIn, user: CurrentUser, db: DB):
    transfer = svc.save_transfer(db, data, user)
    return svc.transfer_out(svc.get_transfer(db, transfer.id))


@router.get("/{transfer_id}", response_model=TransferOut)
def get_transfer(transfer_id: int, _: CurrentUser, db: DB):
    return svc.transfer_out(svc.get_transfer(db, transfer_id))


@router.put("/{transfer_id}", response_model=TransferOut)
def update_transfer(transfer_id: int, data: TransferIn, user: CurrentUser, db: DB):
    svc.save_transfer(db, data, user, svc.get_transfer(db, transfer_id))
    return svc.transfer_out(svc.get_transfer(db, transfer_id))
