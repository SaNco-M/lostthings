from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models import AdModel


class LocationModel(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    ad_id: Mapped[int] = mapped_column(
        ForeignKey("ads.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    latitude: Mapped[float | None]
    longitude: Mapped[float | None]
    address: Mapped[str | None] = mapped_column(String(255))

    ad: Mapped["AdModel"] = relationship(back_populates="location_rel")
