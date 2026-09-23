from datetime import date

from sqlalchemy import BigInteger, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import AuditMixin, Base
from app.models.person import PersonFields
from app.models.user import User
from app.models.vehicle import VehicleFields
from app.models.witness import Witness


class OwnershipTransfer(VehicleFields, AuditMixin, Base):
    """One sale. Keeps a snapshot of the vehicle (columns inherited from VehicleFields)
    and of both parties (TransferParty), so re-printing always gives the same documents."""

    __tablename__ = "ownership_transfers"

    id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_id: Mapped[int | None] = mapped_column(ForeignKey("vehicles.id", ondelete="SET NULL"))
    registration_authority: Mapped[str | None] = mapped_column(String(200))
    sale_price: Mapped[int | None] = mapped_column(BigInteger)
    sale_price_words: Mapped[str | None] = mapped_column(String(300))
    sale_date: Mapped[date]
    fee_bank_name: Mapped[str | None] = mapped_column(String(200))
    notes: Mapped[str | None] = mapped_column(Text)

    parties: Mapped[list["TransferParty"]] = relationship(
        back_populates="transfer", cascade="all, delete-orphan", order_by="TransferParty.id"
    )
    witnesses: Mapped[list[Witness]] = relationship(cascade="all, delete-orphan", order_by=Witness.position)
    created_by: Mapped[User | None] = relationship(foreign_keys="OwnershipTransfer.created_by_id")
    updated_by: Mapped[User | None] = relationship(foreign_keys="OwnershipTransfer.updated_by_id")

    def party(self, role: str) -> "TransferParty":
        return next(p for p in self.parties if p.role == role)

    @property
    def seller(self) -> "TransferParty":
        return self.party("seller")

    @property
    def buyer(self) -> "TransferParty":
        return self.party("buyer")


class TransferParty(PersonFields, Base):
    """Seller or buyer of a transfer, as printed on the forms."""

    __tablename__ = "transfer_parties"
    __table_args__ = (UniqueConstraint("transfer_id", "role", "position"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    transfer_id: Mapped[int] = mapped_column(ForeignKey("ownership_transfers.id", ondelete="CASCADE"), index=True)
    person_id: Mapped[int | None] = mapped_column(ForeignKey("people.id", ondelete="SET NULL"))
    role: Mapped[str] = mapped_column(String(10))  # "seller" | "buyer"
    position: Mapped[int] = mapped_column(default=1)  # >1 reserved for joint owners

    transfer: Mapped[OwnershipTransfer] = relationship(back_populates="parties")
