from typing import Any
from pydantic import BaseModel, ConfigDict, field_validator, computed_field, Field


class AdCreateSchema(BaseModel):
    user_id: int
    category: str = Field(min_length=1, title="Категория объявления")
    color: str | None = Field(min_length=1, title="Цвет")
    ad_type: str = Field(min_length=2, title="Тип объявления")
    breed: str | None = Field(default=None, title="Порода")
    pet_name: str | None = Field(default=None, title="Кличка")
    reward: int| None = Field(default=None, title="Вознаграждение")
    distinctive_features: str | None = Field(default="Нет", max_length=200, title="Особые приметы")
    extra_info: str | None = Field(default=None)

    @field_validator("color")
    @classmethod
    def validate_color(cls, value):
        if "Белый" not in value and "Черный" not in value and "Серый" not in value:
            raise ValueError("Поменяйте цвет")

        return value

    @field_validator("ad_type")
    @classmethod
    def validate_type(cls, ad_type: Any) -> str:
        if ad_type not in ["item", "pet", "human"]:
            raise ValueError("Объявление не может быть такого типа")

        return ad_type


class AdResponseSchema(BaseModel):
    id: int
    category: str
    color: str

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def display_field(self) -> str:
        return f"Найдено: {self.category}, цвет {self.color}"


class UserCreateSchema(BaseModel):
    name: str
    contact_info: str

    @field_validator("contact_info")
    @classmethod
    def validate_contact(cls, value):
        if "@" not in value and "+" not in value:
            raise ValueError("Добавьте + или @")

        return value


class UserResponseSchema(BaseModel):
    id: int
    name: str
    contact_info: str
    role: str


    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def display_name(self) -> str:
        return f"User: {self.name} (ID: {self.id})"


