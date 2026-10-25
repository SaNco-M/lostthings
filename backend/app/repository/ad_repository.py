from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import (
    AdModel,
    ItemAdModel,
    LocationModel,
    PetAdModel,
    PhotoModel,
    UserModel,
)
from app.schemas import AnimalAdCreateSchema


class AdRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_animal_ad(
        self, user_id: int, data: AnimalAdCreateSchema
    ) -> AdModel:
        ad = AdModel(
            user_id=user_id,
            title=data.title,
            description=data.description,
            category=data.category.value,
            listing_type=data.listing_type.value,
            type_ad=data.type_ad.value,
        )

        if data.pet_details:
            PetAdModel(
                pet_name=data.pet_details.pet_name,
                breed=data.pet_details.breed,
                color=data.pet_details.color,
                ad=ad,
            )

        if data.location:
            LocationModel(
                address=data.location,
                ad=ad,
            )

        if data.photo:
            PhotoModel(
                url=data.photo,
                position=0,
                ad=ad,
            )

        self.session.add(ad)
        await self.session.commit()

        return ad

    async def get_by_id(self, ad_id: int) -> AdModel | None:
        query = (
            select(AdModel)
            .where(AdModel.id == ad_id)
            .options(
                selectinload(AdModel.pet_details),
                selectinload(AdModel.location_rel),
                selectinload(AdModel.photos),
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
