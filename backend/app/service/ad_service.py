from app.repository import AdRepository
from app.schemas import AnimalAdCreateSchema, ItemAdCreateSchema


class AdService:
    def __init__(self, repository):
        self.repository = repository

    async def create_animal_ad(self, data: AdRepository, user_id: int):
        pass

    async def create_item_ad(seld, data: ItemAdCreateSchema):
        pass
