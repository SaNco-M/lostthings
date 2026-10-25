from app.exceptions import AdNotFoundError
from app.models import AdModel
from app.repository import AdRepository
from app.schemas import AnimalAdCreateSchema, ItemAdCreateSchema


class AdService:
    def __init__(self, ad_repository: AdRepository):
        self.ad_repository = ad_repository

    async def create_animal_ad(
        self, user_id: int, data: AnimalAdCreateSchema
    ) -> AdModel:

        return await self.ad_repository.create_animal_ad(user_id=user_id, data=data)

    async def get_ad_by_id(self, ad_id: int) -> AdModel:
        ad = await self.ad_repository.get_by_id(ad_id=ad_id)

        if ad is None:
            raise AdNotFoundError(f"Ad {ad_id} not found")

        return ad
