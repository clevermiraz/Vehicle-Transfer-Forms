"""Business logic for ownership transfers: save (with customer/vehicle reuse), search, serialize."""

from sqlalchemy import exists, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models import OwnershipTransfer, Person, TransferParty, User, Vehicle, Witness
from app.models.person import PERSON_FIELDS
from app.models.vehicle import VEHICLE_FIELDS
from app.schemas.person import PersonIn
from app.schemas.transfer import TransferIn
from app.schemas.vehicle import VehicleIn
from app.services.money import amount_in_words
from app.services.normalize import clean_text, digits_only, normalize_phone, normalize_registration


class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


def _person_values(data: PersonIn) -> dict:
    return {f: getattr(data, f) for f in PERSON_FIELDS}


def _vehicle_values(data: VehicleIn) -> dict:
    values = {f: getattr(data, f) for f in VEHICLE_FIELDS if f != "registration_number_norm"}
    values["registration_number"] = values["registration_number"].upper()
    values["registration_number_norm"] = normalize_registration(values["registration_number"])
    return values


def _upsert_person(db: Session, data: PersonIn, user: User) -> Person:
    """Update the picked customer, or the one with the same NID, or create a new one."""
    if data.id is not None:
        person = db.get(Person, data.id)
        if person is None:
            raise NotFoundError("Selected customer no longer exists")
    elif data.nid:
        person = db.scalar(select(Person).where(Person.nid == data.nid))
    else:
        person = None
    if person is None:
        person = Person(created_by_id=user.id)
        db.add(person)
    for field, value in _person_values(data).items():
        setattr(person, field, value)
    person.updated_by_id = user.id
    return person


def _upsert_vehicle(db: Session, data: VehicleIn, user: User) -> Vehicle:
    values = _vehicle_values(data)
    if data.id is not None:
        vehicle = db.get(Vehicle, data.id)
        if vehicle is None:
            raise NotFoundError("Selected vehicle no longer exists")
    else:
        vehicle = db.scalar(select(Vehicle).where(Vehicle.registration_number_norm == values["registration_number_norm"]))
    if vehicle is None:
        vehicle = Vehicle(created_by_id=user.id)
        db.add(vehicle)
    for field, value in values.items():
        setattr(vehicle, field, value)
    vehicle.updated_by_id = user.id
    return vehicle


def save_transfer(db: Session, data: TransferIn, user: User, transfer: OwnershipTransfer | None = None) -> OwnershipTransfer:
    """Create or update a transfer in ONE database transaction.

    The reusable Person/Vehicle records are updated for future auto-fill, and the transfer
    keeps its own snapshot of the values so its documents never change afterwards by accident.
    """
    try:
        seller = _upsert_person(db, data.seller, user)
        buyer = _upsert_person(db, data.buyer, user)
        vehicle = _upsert_vehicle(db, data.vehicle, user)
        db.flush()

        if transfer is None:
            transfer = OwnershipTransfer(created_by_id=user.id)
            db.add(transfer)
        transfer.updated_by_id = user.id
        transfer.vehicle_id = vehicle.id
        for field, value in _vehicle_values(data.vehicle).items():
            setattr(transfer, field, value)
        for field in ("registration_authority", "sale_price", "sale_date", "fee_bank_name", "notes"):
            setattr(transfer, field, getattr(data, field))
        transfer.sale_price_words = data.sale_price_words or (
            amount_in_words(data.sale_price) if data.sale_price else None
        )

        # Replace parties and witnesses. Flush the removals first so the
        # (transfer_id, role, position) unique constraint never sees duplicates.
        transfer.parties.clear()
        transfer.witnesses.clear()
        db.flush()
        for role, person, person_data in (("seller", seller, data.seller), ("buyer", buyer, data.buyer)):
            transfer.parties.append(
                TransferParty(role=role, position=1, person_id=person.id, **_person_values(person_data))
            )
        transfer.witnesses.extend(
            Witness(position=i, name=w.name, address=w.address, phone=w.phone)
            for i, w in enumerate(data.witnesses, start=1)
        )
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ConflictError(_conflict_message(exc)) from None
    except Exception:
        db.rollback()
        raise
    db.refresh(transfer)
    return transfer


def _conflict_message(exc: IntegrityError) -> str:
    text = str(exc.orig)
    if "people_nid" in text:
        return "This NID already belongs to another saved customer. Search for that customer and select them."
    if "vehicles_registration_number_norm" in text:
        return "This registration number already belongs to another saved vehicle. Search for it and select it."
    return "This record conflicts with existing data."


def get_transfer(db: Session, transfer_id: int) -> OwnershipTransfer:
    transfer = db.scalar(
        select(OwnershipTransfer)
        .where(OwnershipTransfer.id == transfer_id)
        .options(
            selectinload(OwnershipTransfer.parties),
            selectinload(OwnershipTransfer.witnesses),
            selectinload(OwnershipTransfer.created_by),
            selectinload(OwnershipTransfer.updated_by),
        )
    )
    if transfer is None:
        raise NotFoundError("Transfer not found")
    return transfer


def search_transfers(db: Session, q: str | None, limit: int = 50) -> list[OwnershipTransfer]:
    """Match registration number, NID, mobile, seller name or buyer name. Empty q = latest."""
    stmt = (
        select(OwnershipTransfer)
        .options(selectinload(OwnershipTransfer.parties))
        .order_by(OwnershipTransfer.created_at.desc())
        .limit(limit)
    )
    q = clean_text(q)
    if q:
        party_match = [TransferParty.name.icontains(q, autoescape=True)]
        digits = digits_only(q).lstrip("+")
        if digits.isdigit():
            party_match.append(TransferParty.nid.contains(digits, autoescape=True))
            party_match.append(TransferParty.phone.contains(normalize_phone(q), autoescape=True))
        conditions = [exists().where(TransferParty.transfer_id == OwnershipTransfer.id, or_(*party_match))]
        reg = normalize_registration(q)
        if reg:
            conditions.append(OwnershipTransfer.registration_number_norm.contains(reg, autoescape=True))
        if digits.isdigit() and len(digits) <= 9:  # transfer number (NIDs are longer)
            conditions.append(OwnershipTransfer.id == int(digits))
        stmt = stmt.where(or_(*conditions))
    return list(db.scalars(stmt))


def search_people(db: Session, q: str, limit: int = 10) -> list[Person]:
    q = clean_text(q) or ""
    if len(q) < 2:
        return []
    conditions = [Person.name.icontains(q, autoescape=True)]
    digits = digits_only(q).lstrip("+")
    if digits.isdigit():
        conditions += [
            Person.nid.contains(digits, autoescape=True),
            Person.phone.contains(normalize_phone(q), autoescape=True),
        ]
    return list(db.scalars(select(Person).where(or_(*conditions)).order_by(Person.updated_at.desc()).limit(limit)))


def search_vehicles(db: Session, q: str, limit: int = 10) -> list[Vehicle]:
    q = clean_text(q) or ""
    if len(q) < 2:
        return []
    conditions = [
        Vehicle.chassis_number.icontains(q, autoescape=True),
        Vehicle.engine_number.icontains(q, autoescape=True),
    ]
    reg = normalize_registration(q)
    if reg:
        conditions.append(Vehicle.registration_number_norm.contains(reg, autoescape=True))
    return list(db.scalars(select(Vehicle).where(or_(*conditions)).order_by(Vehicle.updated_at.desc()).limit(limit)))


def last_used_defaults(db: Session) -> dict:
    """Registration authority and fee bank from the most recent transfer that has them."""
    def latest(column):
        return db.scalar(
            select(column).where(column.is_not(None)).order_by(OwnershipTransfer.created_at.desc()).limit(1)
        )

    return {
        "registration_authority": latest(OwnershipTransfer.registration_authority),
        "fee_bank_name": latest(OwnershipTransfer.fee_bank_name),
    }


def _party_dict(party: TransferParty) -> dict:
    return {"id": party.person_id, **{f: getattr(party, f) for f in PERSON_FIELDS}}


def transfer_to_dict(transfer: OwnershipTransfer) -> dict:
    """Same shape as SAMPLE_DATA.json (used for PDFs) plus ids/audit info (used by the API)."""
    vehicle = {f: getattr(transfer, f) for f in VEHICLE_FIELDS if f != "registration_number_norm"}
    return {
        "seller": _party_dict(transfer.seller),
        "buyer": _party_dict(transfer.buyer),
        "vehicle": {"id": transfer.vehicle_id, **vehicle},
        "transfer": {
            "id": transfer.id,
            "registration_authority": transfer.registration_authority,
            "sale_price": transfer.sale_price,
            "sale_price_words": transfer.sale_price_words,
            "sale_date": transfer.sale_date,
            "fee_bank_name": transfer.fee_bank_name,
            "notes": transfer.notes,
            "witnesses": [
                {"position": w.position, "name": w.name, "address": w.address, "phone": w.phone}
                for w in transfer.witnesses
            ],
        },
    }


def transfer_out(transfer: OwnershipTransfer) -> dict:
    data = transfer_to_dict(transfer)
    return {
        **data["transfer"],
        "seller": data["seller"],
        "buyer": data["buyer"],
        "vehicle": data["vehicle"],
        "created_at": transfer.created_at,
        "updated_at": transfer.updated_at,
        "created_by": transfer.created_by.name if transfer.created_by else None,
        "updated_by": transfer.updated_by.name if transfer.updated_by else None,
    }


def list_item(transfer: OwnershipTransfer) -> dict:
    return {
        "id": transfer.id,
        "registration_number": transfer.registration_number,
        "seller_name": transfer.seller.name,
        "buyer_name": transfer.buyer.name,
        "sale_date": transfer.sale_date,
        "created_at": transfer.created_at,
    }
