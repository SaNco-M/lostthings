from typing import TYPE_CHECKING

from database import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models import AdModel


class PetAdModel(Base):
    __tablename__ = "pet_ads"

    id: Mapped[int] = mapped_column(primary_key=True)
    ad_id: Mapped[int] = mapped_column(ForeignKey("ads.id"), unique=True)
    pet_name: Mapped[str | None] = mapped_column(String(50))
    breed: Mapped[str | None] = mapped_column(String(50), index=True)
    color: Mapped[str | None] = mapped_column(String(100), index=True)

    ad: Mapped["AdModel"] = relationship(back_populates="pet_details")

