from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models import AdModel


class ItemAdModel(Base):
    __tablename__ = "item_ads"

    id: Mapped[int] = mapped_column(primary_key=True)

    ad_id: Mapped[int] = mapped_column(
        ForeignKey("ads.id"), unique=True, nullable=False
    )

    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    model: Mapped[str | None] = mapped_column(String(100), index=True)
    brand: Mapped[str | None] = mapped_column(String(100), index=True)
    color: Mapped[str | None] = mapped_column(String(100), index=True)

    ad: Mapped["AdModel"] = relationship(back_populates="item_details")
