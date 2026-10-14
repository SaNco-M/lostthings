from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from database import Base
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models import AdModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    contact_info: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now,
    )
    role: Mapped[str] = mapped_column(String(20), default="user")

    ads: Mapped[list[AdModel]] = relationship(back_populates="author")
