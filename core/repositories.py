from sqlalchemy.exc import IntegrityError

from sqlalchemy import select
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from exceptions import IdError
from models import UserModel, AdModel, ItemAdModel, PetAdModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int):
        user = await self.session.get(UserModel, user_id)
        if user is None:
            raise IdError("Такого пользователя с таким айди нет")
        return user

    async def get_all_users(self):
        stmt = select(UserModel).options(selectinload(UserModel.user_ads))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add(self, name: str, contact_info: str) -> UserModel | None:
        user = UserModel(name=name, contact_info=contact_info)

        try:
            self.session.add(user)
            await self.session.commit()
            return user

        except IntegrityError:
            await self.session.rollback()


class AdRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_pet_ad(
            self,
            user_id: int,
            category: str,
            color: str,
            pet_name: str | None = None,
            breed: str | None = None,
            **kwargs
    ):
        user = await self.session.get(UserModel, user_id)
        if user is None:
            raise IdError("Такого пользователя с таким айди нет")

        pet_ad = PetAdModel(
            user_id=user_id,
            author=user.name,
            category=category,
            color=color,
            pet_name=pet_name,
            breed=breed,
            extra_info=json.dumps(kwargs)
        )

        try:
            self.session.add(pet_ad)
            await self.session.commit()
            return pet_ad
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Невозможно добавить объявление, ошибка: {e}")

    async def add_item_ad(
            self,
            user_id: int,
            category: str,
            color: str,
            value: str | None = None,
            **kwargs
    ):
        user = await self.session.get(UserModel, user_id)
        if user is None:
            raise IdError("Такого пользователя с таким айди нет")

        item_ad = ItemAdModel(
            user_id=user_id,
            author=user.name,
            category=category,
            color=color,
            value=value,
            extra_info=json.dumps(kwargs)
        )

        try:
            self.session.add(item_ad)
            await self.session.commit()
            return item_ad

        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Невозможно добавить объявление, ошибка: {e}")

    async def get_all_ads(self):
        stmt = select(AdModel)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def filter(self, limit: int, offset: int, category: str | None = None, color: str | None = None):
        stmt = select(AdModel)

        conditions = []

        if category:
            conditions.append(AdModel.category == category)

        if color:
            conditions.append(AdModel.color == color)

        if conditions:
            stmt = stmt.where(*conditions)

        stmt = stmt.limit(limit).offset(offset)

        result = await self.session.execute(stmt)

        return result.scalars().all()
