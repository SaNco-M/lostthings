from typing import Iterator

from models import Ad, User
from exceptions import IdError
from utils import admin_required, type_check, time_logger

class LostAndFound:
    """Главный класс системы"""

    def __init__(self) -> None:
        self.__users = {}

    def __iter__(self) -> Iterator:
        for user in self.__users.values():
            for ad in user.get_ads():
                yield ad

    def __call__(self, lost_ad: Ad) -> list[Ad]:
        res = [
            ad
            for user in self.__users.values()
            for ad in user.get_ads()
            if ad.match(lost_ad)
        ]

        return res

    def get_list_users(self) -> list[User]:
        return list(self.__users.values())

    @type_check(user_id=int, name=str, contact_info=str)
    def register_user(self, user_id, name, contact_info):
        if user_id in self.__users:
            raise IdError("Ошибка, айди занят")
        self.__users[user_id] = User(user_id, name, contact_info)
        print('Пользователь добавлен')

    def post_ad_to_user(self, user_id: int, **kwargs):
        """Добавление объявления пользователю"""
        if user_id in self.__users:
            self.__users.get(user_id).create_ad(**kwargs)
        else:
            raise IdError('Такого пользователя нет')

    @admin_required
    def force_delete_ad(self, initiator: User, user_id: int, ad_index: int):
        pass

    def verify_user_ad(self, user_id: int, ad_index: int):
        if not user_id in self.__users:
            raise IdError('Такого пользователя нет')
        user = self.__users[user_id]
        ads = user.get_ads()
        ad = ads[ad_index]
        ad.verify()
        ad.publish()

    def get_system_stats(self) -> dict[str, int]:
        return {i.name: len(i.get_ads()) for i in self.__users.values()}

    def filter_ads(self, category: str | None, status: str | None, author_name: str | None) -> list[Ad]:
        """Фильтры объявлений"""
        result = [
            ad
            for user in self.__users.values()
            for ad in user.get_ads()
            if (
                    (category is None or ad.category.lower() == category.lower())
                    and (status is None or ad.status.lower() == status.lower())
                    and (author_name is None or ad.author.lower() == author_name.lower())
            )
        ]
        return result

    def bulk_publish(self, user_id: int) -> list[str | None]:
        """Публикует все объявления"""
        errors = []
        if user_id not in self.__users:
            raise IdError('Такого пользователя нет')
        for ad in self.__users[user_id].get_ads():
            try:
                ad.publish()
            except ValueError as e:
                errors.append(str(e))
        return errors
