from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.enums import AdType, ItemCategory, LostOrFound


class ItemDetailsResponse(BaseModel):
    model: str | None = Field(max_length=100, default=None)
    brand: str | None = Field(max_length=100, default=None)
    color: str | None = Field(max_length=100, default=None)


class ItemAdCreateSchema(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=3, max_length=300)
    category: ItemCategory = Field(title="Категория объявления")
    listing_type: LostOrFound
    location: str = Field(min_length=2, max_length=200)
    photo: str | None = Field(default=None)
    item_details: ItemDetailsResponse | None = None
    type_ad: Literal[AdType.ITEM] = AdType.ITEM


class ItemAdResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    photo: str | None
    item_details: ItemDetailsResponse | None = None
    listing_type: LostOrFound
    category: ItemCategory
    title: str
    description: str
    location: str
    created_at: datetime
    type_ad: AdType
