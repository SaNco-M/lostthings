from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.repository import AdRepository
from app.service import AdService


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


def get_ad_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> AdRepository:
    return AdRepository(session=session)


def get_ad_service(
    repository: Annotated[AdRepository, Depends(get_ad_repository)],
) -> AdService:
    return AdService(ad_repository=repository)
