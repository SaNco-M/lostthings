from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select
import json

from exceptions import IdError
from models import UserModel, AdModel, ItemAdModel, PetAdModel


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int):
        user = self.session.get(UserModel, user_id)
        if user is None:
            raise IdError("Такого пользователя с таким айди нет")
        return user

    def get_all_users(self):
        stmt = select(UserModel)
        result = self.session.execute(stmt)
        return result.scalars().all()

    def add(self, name: str, contact_info: str) -> UserModel | None:
        user = UserModel(name=name, contact_info=contact_info)

        try:
            self.session.add(user)
            self.session.commit()
            return user

        except IntegrityError as e:
            self.session.rollback()
            raise Exception(f"Невозможно добавить пользователя, ошибка: {e}")


class AdRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_pet_ad(
            self,
            user_id: int,
            category: str,
            color: str,
            pet_name: str | None = None,
            breed: str | None = None,
            **kwargs
    ):
        user = self.session.get(UserModel, user_id)
        if user is None:
            raise IdError("Такого пользователя с таким айди нет")

        pet_ad = PetAdModel(
            author=user.name,
            category=category,
            color=color,
            pet_name=pet_name,
            breed=breed,
            extra_info=json.dumps(kwargs)
        )

        try:
            self.session.add(pet_ad)
            self.session.commit()
            return pet_ad
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Невозможно добавить объявление, ошибка: {e}")

    def add_item_ad(
            self,
            user_id: int,
            category: str,
            color: str,
            value: str | None = None,
            **kwargs
    ):
        user = self.session.get(UserModel, user_id)
        if user is None:
            raise IdError("Такого пользователя с таким айди нет")

        item_ad = ItemAdModel(
            author=user.name,
            category=category,
            color=color,
            value=value,
            extra_info=json.dumps(kwargs)
        )

        try:
            self.session.add(item_ad)
            self.session.commit()
            return item_ad

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Невозможно добавить объявление, ошибка: {e}")

    def get_all_ads(self):
        stmt = select(AdModel)
        result = self.session.execute(stmt)
        return result.scalars().all()

    def filter(self, category: str | None = None, color: str | None = None):
        stmt = select(AdModel)

        conditions = []

        if category:
            conditions.append(AdModel.category == category)

        if color:
            conditions.append(AdModel.color == color)

        if conditions:
            stmt = stmt.where(*conditions)

        result = self.session.execute(stmt)
        return result.scalars().all()
