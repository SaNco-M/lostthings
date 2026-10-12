from backend.app.core import AdRepository, UserRepository
from backend.app.models import AdModel, ItemAdModel, PetAdModel
from backend.app.utils import admin_required, type_check
from sqlalchemy.ext.asyncio import AsyncSession


class LostAndFound:
    """Main class of the system"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.ad_repo = AdRepository(session)

    async def __call__(self, lost_ad) -> list[AdModel]:
        res = [ad for ad in await self.ad_repo.get_all_ads() if ad.match(lost_ad)]

        return res

    async def get_all_ads(self):
        return await self.ad_repo.get_all_ads()

    async def get_list_users(self):
        return await self.user_repo.get_all_users()

    @type_check(name=str, contact_info=str)
    async def register_user(self, name, contact_info):
        await self.user_repo.add(name=name, contact_info=contact_info)

        return await self.user_repo.add(name=name, contact_info=contact_info)

    async def post_ad_to_user(self, user_id: int, ad_class, **kwargs):
        """Добавление объявления пользователю"""

        if ad_class == PetAdModel:
            return await self.ad_repo.add_pet_ad(user_id=user_id, **kwargs)

        elif ad_class == ItemAdModel:
            return await self.ad_repo.add_item_ad(user_id=user_id, **kwargs)

    @admin_required
    def force_delete_ad(self, initiator, user_id: int, ad_index: int):
        pass

    async def verify_user_ad(self, user_id: int, ad_index: int) -> None:
        user = await self.user_repo.get_by_id(user_id)
        ad = user.user_ads[ad_index]
        ad.verify()
        ad.publish()
        await self.session.commit()

    async def get_system_stats(self) -> dict[str, int]:
        return {i.name: len(i.user_ads) for i in await self.user_repo.get_all_users()}

    async def filter_ads(
        self,
        limit: int,
        offset: int,
        category: str | None = None,
        color: str | None = None,
    ):
        """Фильтры объявлений"""
        return await self.ad_repo.filter(
            limit=limit, offset=offset, category=category, color=color
        )

    @admin_required
    async def bulk_publish(self, user_id: int) -> list[str | None]:
        """Публикует все объявления"""
        errors = []

        await self.user_repo.get_by_id(user_id)
        for ad in await self.ad_repo.get_all_ads():
            try:
                ad.publish()
                await self.session.commit()
            except ValueError as e:
                await self.session.rollback()
                errors.append(str(e))
        return errors
