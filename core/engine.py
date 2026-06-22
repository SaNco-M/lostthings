from typing import Iterator

from sqlalchemy.orm import Session

from core import UserRepository, AdRepository
from models import Ad, User, AdModel, PetAdModel, ItemAdModel
from utils import admin_required, type_check


class LostAndFound:
    """Главный класс системы"""

    def __init__(self, session: Session):
        self.session = session
        self.user_repo = UserRepository(session)
        self.ad_repo = AdRepository(session)

    def __iter__(self) -> Iterator:
        for ad in self.ad_repo.get_all_ads():
            yield ad

    def __call__(self, lost_ad: Ad) -> list[AdModel]:
        res = [
            ad
            for ad in self.ad_repo.get_all_ads()
            if ad.match(lost_ad)
        ]

        return res

    def get_list_users(self):
        return self.user_repo.get_all_users()

    @type_check(name=str, contact_info=str)
    def register_user(self, name, contact_info):
        self.user_repo.add(name=name, contact_info=contact_info)
        print('Пользователь добавлен')

    def post_ad_to_user(self, user_id: int, ad_class, **kwargs):
        """Добавление объявления пользователю"""

        if ad_class == PetAdModel:
            self.ad_repo.add_pet_ad(user_id=user_id, **kwargs)

        elif ad_class == ItemAdModel:
            self.ad_repo.add_item_ad(user_id=user_id, **kwargs)

    @admin_required
    def force_delete_ad(self, initiator: User, user_id: int, ad_index: int):
        pass

    def verify_user_ad(self, user_id: int, ad_index: int) -> None:
        user = self.user_repo.get_by_id(user_id)
        ad = user.user_ads[ad_index]
        ad.verify()
        ad.publish()
        self.session.commit()

    def get_system_stats(self) -> dict[str, int]:
        return {i.name: len(i.user_ads) for i in self.user_repo.get_all_users()}

    def filter_ads(self, category: str | None = None, color: str | None = None):
        """Фильтры объявлений"""
        return self.ad_repo.filter(category=category, color=color)

    @admin_required
    def bulk_publish(self, user_id: int) -> list[str | None]:
        """Публикует все объявления"""
        errors = []

        self.user_repo.get_by_id(user_id)
        for ad in self.ad_repo.get_all_ads():
            try:
                ad.publish()
                self.session.commit()
            except ValueError as e:
                self.session.rollback()
                errors.append(str(e))
        return errors
