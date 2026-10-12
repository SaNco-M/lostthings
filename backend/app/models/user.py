from database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, validates


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    contact_info: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    role: Mapped[str] = mapped_column(default="user")

    @validates("contact_info")
    def validate_contact(self, key, contact: str) -> str:
        if "@" not in contact and "+" not in contact:
            raise ValueError("Добавьте + или @")

        return contact
