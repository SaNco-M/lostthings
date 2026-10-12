from database import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class PetAdModel(Base):
    __tablename__ = "pet_ads"

    id: Mapped[int] = mapped_column(ForeignKey("ads.id"), primary_key=True)
    breed: Mapped[str] = mapped_column(String(100))
    pet_name: Mapped[str | None] = mapped_column(String(100))

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

        other_breed = getattr(other_ad, "breed", None)
        return self.breed == other_breed
