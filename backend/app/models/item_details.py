from database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class ItemAdModel(Base):
    __tablename__ = "item_ads"

    id: Mapped[int] = mapped_column(ForeignKey("ads.id"), primary_key=True)
