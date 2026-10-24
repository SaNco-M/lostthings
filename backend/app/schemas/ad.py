from app.enums import AnimalCategory, ItemCategory, TypeAd
from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator


class AnimalAdCreateSchema(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=3, max_length=300)
    category: AnimalCategory = Field(title="Категория объявления")
    pet_name: str | None = Field(default=None, max_length=50)
    breed: str | None = Field(default=None, max_length=50)
    color: str | None = Field(default=None, max_length=100)
    listing_type: TypeAd
    location: str = Field(min_length=2, max_length=200)
    photo: str | None = Field(default=None)


class AnimalAdResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ItemAdCreateSchema(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=3, max_length=300)
    category: ItemCategory = Field(title="Категория объявления")
    listing_type: TypeAd
    location: str = Field(min_length=2, max_length=200)
    photo: str | None

    model: str | None = Field(max_length=100, default=None)
    brand: str | None = Field(max_length=100, default=None)
    color: str | None = Field(max_length=100, default=None)


class ItemAdResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
