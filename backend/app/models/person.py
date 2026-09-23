from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import AuditMixin, Base

PERSON_FIELDS = (
    "name", "father_name", "mother_name", "spouse_name", "father_or_husband_pref",
    "guardian_name", "gender", "date_of_birth", "nationality", "nid", "tin", "phone",
    "present_address", "permanent_address",
)


class PersonFields:
    """Personal details. Shared by the reusable Person record and the per-transfer snapshot."""

    name: Mapped[str] = mapped_column(String(200))
    father_name: Mapped[str | None] = mapped_column(String(200))
    mother_name: Mapped[str | None] = mapped_column(String(200))
    spouse_name: Mapped[str | None] = mapped_column(String(200))
    # Which name goes on the "পিতা/স্বামী" line of Forms 20/21/22: "father" or "husband".
    father_or_husband_pref: Mapped[str] = mapped_column(String(10), default="father", server_default="father")
    guardian_name: Mapped[str | None] = mapped_column(String(200))
    gender: Mapped[str | None] = mapped_column(String(10))
    date_of_birth: Mapped[date | None]
    nationality: Mapped[str | None] = mapped_column(String(50))
    nid: Mapped[str | None] = mapped_column(String(17), index=True)
    tin: Mapped[str | None] = mapped_column(String(12))
    phone: Mapped[str | None] = mapped_column(String(11), index=True)
    present_address: Mapped[str | None] = mapped_column(String(500))
    permanent_address: Mapped[str | None] = mapped_column(String(500))


class Person(PersonFields, AuditMixin, Base):
    """Reusable customer record used to auto-fill seller/buyer details."""

    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    nid: Mapped[str | None] = mapped_column(String(17), unique=True)
