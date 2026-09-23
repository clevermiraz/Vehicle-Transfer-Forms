from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import AuditMixin, Base

VEHICLE_FIELDS = (
    "registration_number", "registration_number_norm", "vehicle_type", "chassis_number",
    "engine_number", "manufacturer", "manufacturing_year", "previous_registration_number",
)


class VehicleFields:
    """Vehicle details. Shared by the reusable Vehicle record and the per-transfer snapshot."""

    registration_number: Mapped[str] = mapped_column(String(50))
    # Upper-case, letters/digits only: used for search and duplicate detection.
    registration_number_norm: Mapped[str] = mapped_column(String(50), index=True)
    vehicle_type: Mapped[str | None] = mapped_column(String(100))
    chassis_number: Mapped[str | None] = mapped_column(String(50), index=True)
    engine_number: Mapped[str | None] = mapped_column(String(50))
    manufacturer: Mapped[str | None] = mapped_column(String(100))
    manufacturing_year: Mapped[int | None]
    previous_registration_number: Mapped[str | None] = mapped_column(String(50))


class Vehicle(VehicleFields, AuditMixin, Base):
    """Reusable vehicle record used to auto-fill vehicle details."""

    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    registration_number_norm: Mapped[str] = mapped_column(String(50), unique=True)
