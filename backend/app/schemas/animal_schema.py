from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.enums import AdType, AnimalCategory, LostOrFound


class AnimalDetailsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pet_name: str | None = Field(default=None, max_length=50)
    breed: str | None = Field(default=None, max_length=50)
    color: str | None = Field(default=None, max_length=100)


class AnimalAdCreateSchema(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=3, max_length=300)
    category: AnimalCategory = Field(title="Категория объявления")
    listing_type: LostOrFound
    location: str = Field(min_length=2, max_length=200)
    photo: str | None = Field(default=None)
    pet_details: AnimalDetailsResponse | None = None
    type_ad: Literal[AdType.ANIMAL] = AdType.ANIMAL


class AnimalAdResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    photo: str | None
    pet_details: AnimalDetailsResponse | None = None
    listing_type: LostOrFound
    category: AnimalCategory
    title: str
    description: str
    location: str
    created_at: datetime
    type_ad: AdType
