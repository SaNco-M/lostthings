from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models import AdModel


class PetAdModel(Base):
    __tablename__ = "pet_ads"

    id: Mapped[int] = mapped_column(primary_key=True)
    ad_id: Mapped[int] = mapped_column(
        ForeignKey("ads.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    pet_name: Mapped[str | None] = mapped_column(String(50))
    breed: Mapped[str | None] = mapped_column(String(50), index=True)
    color: Mapped[str | None] = mapped_column(String(100), index=True)

    ad: Mapped["AdModel"] = relationship(back_populates="pet_details")