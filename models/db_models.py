from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from typing import List
from config import DEFAULT_STATUS
from sqlalchemy.orm import validates

class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    contact_info: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    role: Mapped[str] = mapped_column(default="user")

    user_ads: Mapped[List["AdModel"]] = relationship(back_populates="user")

    @validates("contact_info")
    def validate_contact(self, key, contact: str) -> str:
        if "@" not in contact and "+" not in contact:
            raise ValueError("Добавьте + или @")

        return contact

    __mapper_args__ = {
        "polymorphic_on": "role",
        "polymorphic_identity": "user",
    }


class AdModel(Base):
    __tablename__ = "ads"

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(String(50), nullable=False)
    category: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    color: Mapped[str | None] = mapped_column(String(50), index=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    status: Mapped[str] = mapped_column(String(50), default=DEFAULT_STATUS)
    extra_info: Mapped[str | None] = mapped_column(String(100), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    ad_type: Mapped[str]
    user: Mapped[UserModel] = relationship(back_populates="user_ads")

    __mapper_args__ = {
        "polymorphic_on": "ad_type",
        "polymorphic_identity": "ad",
    }

    def __str__(self):
        if self.extra_info:
            return (
                f"Описание: {self.category}, {self.color}, "
                f"(Автор: {self.author}), Доп. Инф: {self.extra_info}"
            )
        else:
            return (
                f"Описание:"
                f" {self.category},"
                f" {self.color},"
                f" (Автор: {self.author})"
            )


    def verify(self):
        self.is_verified = True

    def publish(self):
        if not self.is_verified:
            raise ValueError("Объявление не проверено")
        self.status = "published"

    def get_search_text(self):
        return f"{self.category} {self.color} {self.author}"

    def match(self, other_ad: "AdModel") -> bool:
        """Ищет совпадения по категории"""
        return self.category == other_ad.category


class PetAdModel(AdModel):
    __tablename__ = "pet_ads"

    id: Mapped[int] = mapped_column(ForeignKey("ads.id"), primary_key=True)
    breed: Mapped[str] = mapped_column(String(100))
    pet_name: Mapped[str | None] = mapped_column(String(100))

    __mapper_args__ = {
        "polymorphic_identity": "pet_ad",
    }

    def __str__(self):
        parent_str = super().__str__()
        if self.pet_name:
            return f"{parent_str}, Порода {self.breed}, Имя {self.pet_name}"
        else:
            return parent_str + f"Порода {self.breed}"

    def get_search_text(self):
        return f"{self.category} {self.color} {self.breed} {self.pet_name}"

    def match(self, other_ad):
        """Ищет совпадения по категории и породе"""
        if not super().match(other_ad):
            return False

        other_breed = getattr(other_ad, 'breed', None)
        return self.breed == other_breed


class ItemAdModel(AdModel):
    __tablename__ = "item_ads"

    id: Mapped[int] = mapped_column(ForeignKey("ads.id"), primary_key=True)
    value: Mapped[int | None] = mapped_column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "item_ad",
    }

    def __str__(self):
        parent_str = super().__str__()
        if self.value:
            return f"{parent_str}, Примерная стоимость: {self.value}"
        else:
            return parent_str

    def get_search_text(self):
        return f"{self.category} {self.color} {self.value}"

    def match(self, other_ad):
        """Ищет совпадения по категории и цене +- 20%"""
        if not super().match(other_ad):
            return False

        other_value = getattr(other_ad, 'value', None)
        if other_value is None:
            return False
        return 0.8 * other_value <= self.value <= 1.2 * other_value

class AdminModel(UserModel):
    __mapper_args__ = {"polymorphic_identity": "Admin"}