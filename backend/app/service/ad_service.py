from app.exceptions import AdNotFoundError
from app.models import AdModel
from app.repository import AdRepository
from app.schemas import AnimalAdCreateSchema, AnyAdCreateSchema, ItemAdCreateSchema


class AdService:
    def __init__(self, ad_repository: AdRepository):
        self.ad_repository = ad_repository

    async def create_ad(self, user_id: int, data: AnyAdCreateSchema):
        if isinstance(data, AnimalAdCreateSchema):
            return await self.ad_repository.create_animal_ad(user_id=user_id, data=data)
        elif isinstance(data, ItemAdCreateSchema):
            # Ветка для вещей не дописана
            raise NotImplementedError("Создание вещей будет доступно позже")

    async def get_ad_by_id(self, ad_id: int) -> AdModel:
        ad = await self.ad_repository.get_by_id(ad_id=ad_id)

        if ad is None:
            raise AdNotFoundError(f"Ad {ad_id} not found")

        return ad

    async def get_all_ads(self, limit: int = 50, offset: int = 0) -> list[AdModel]:
        return await self.ad_repository.get_all(limit=limit, offset=offset)
