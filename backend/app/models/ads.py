from datetime import datetime
from typing import TYPE_CHECKING

from database import Base
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models import ItemAdModel, PetAdModel, UserModel


class AdModel(Base):
    __tablename__ = "ads"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(300))
    category: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    archived_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="Active")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now,
    )
    ad_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    author: Mapped["UserModel"] = relationship(back_populates="ad")
    pet_details: Mapped["PetAdModel"] = relationship(
        back_populates="ads", uselist=False
    )
    item_details: Mapped["ItemAdModel"] = relationship(
        back_populates="ads", uselist=False
    )
