from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Witness(Base):
    __tablename__ = "witnesses"

    id: Mapped[int] = mapped_column(primary_key=True)
    transfer_id: Mapped[int] = mapped_column(ForeignKey("ownership_transfers.id", ondelete="CASCADE"), index=True)
    position: Mapped[int]  # 1..3, matches the numbered slots on Form 22
    name: Mapped[str] = mapped_column(String(200))
    address: Mapped[str | None] = mapped_column(String(500))
    phone: Mapped[str | None] = mapped_column(String(11))
