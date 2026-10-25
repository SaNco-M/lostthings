from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models import (
        ItemAdModel,
        LocationModel,
        PetAdModel,
        PhotoModel,
        ReportModel,
        UserModel,
    )


class AdModel(Base):
    __tablename__ = "ads"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(300))
    category: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    status: Mapped[str] = mapped_column(String(50), default="Active")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    listing_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    type_ad: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    author: Mapped["UserModel"] = relationship(back_populates="ad")
    pet_details: Mapped["PetAdModel"] = relationship(
        back_populates="ad", uselist=False, cascade="all, delete-orphan"
    )
    item_details: Mapped["ItemAdModel"] = relationship(
        back_populates="ad", uselist=False, cascade="all, delete-orphan"
    )
    photos: Mapped[list["PhotoModel"]] = relationship(
        back_populates="ad", cascade="all, delete-orphan"
    )
    location_rel: Mapped["LocationModel | None"] = relationship(
        back_populates="ad", uselist=False, cascade="all, delete-orphan"
    )
    reports: Mapped[list["ReportModel"]] = relationship(back_populates="ad")

    @property
    def location(self) -> str | None:
        return self.location_rel.address if self.location_rel else None

    @property
    def photo(self) -> str | None:
        return self.photos[0].url if self.photos else None
