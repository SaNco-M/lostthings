"""Временный костыль пока нету функции создания юзера"""

import asyncio
from app.database.session import AsyncSessionLocal
from app.models import UserModel


async def seed_user():
    async with AsyncSessionLocal() as session:

        existing_user = await session.get(UserModel, 1)
        if existing_user:
            print("Пользователь с id=1 уже существует. Пропускаем.")
            return


        user = UserModel(
            id=1,
            name="Тестовый Пользователь",
            email="test@lostthings.ru",
            hashed_password="mock_hashed_secret_password",
        )

        session.add(user)
        await session.commit()
        print("✅ Тестовый пользователь с id=1 успешно создан!")


if __name__ == "__main__":
    asyncio.run(seed_user())
