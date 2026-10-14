import os

os.environ["DATABASE_URL"] = "postgresql+asyncpg://alex:mysecretpass@localhost:5432/lostthings_db"
import pytest
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.main import app, engine, get_db

alembic_cfg = Config("alembic.ini")


@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def test_db():
    command.upgrade(alembic_cfg, "head")

    yield


@pytest.fixture(scope="function", autouse=True)
async def db_session():
    async with engine.connect() as connection:
        async with connection.begin() as transaction:
            async with AsyncSession(bind=connection, expire_on_commit=False) as session:
                async def _override_get_db():
                    yield session

                app.dependency_overrides[get_db] = _override_get_db

                yield session

                await transaction.rollback()
                app.dependency_overrides.clear()
