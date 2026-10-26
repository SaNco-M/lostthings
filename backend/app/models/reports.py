from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models import AdModel, UserModel


class ReportModel(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    reporter_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    ad_id: Mapped[int] = mapped_column(ForeignKey("ads.id"))
    reason: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(50), default="not_checked")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now,
    )
    author: Mapped["UserModel"] = relationship(back_populates="reports")

    ad: Mapped["AdModel"] = relationship(back_populates="reports")
