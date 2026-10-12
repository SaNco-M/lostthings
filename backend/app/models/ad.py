from config import settings
from database import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class AdModel(Base):
    __tablename__ = "ads"

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(String(50), nullable=False)
    category: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    color: Mapped[str | None] = mapped_column(String(50), index=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    status: Mapped[str] = mapped_column(String(50), default=settings.DEFAULT_STATUS)
    extra_info: Mapped[str | None] = mapped_column(String(100), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    reward: Mapped[int | None] = mapped_column(nullable=True)
    ad_type: Mapped[str]

    def __str__(self):
        if self.extra_info:
            return (
                f"Описание: {self.category}, {self.color}, "
                f"(Автор: {self.author}), Доп. Инф: {self.extra_info}"
            )
        else:
            return f"Описание: {self.category}, {self.color}, (Автор: {self.author})"

    def verify(self):
        self.is_verified = True

    def publish(self):
        if not self.is_verified:
            raise ValueError("Объявление не проверено")
        self.status = "published"
