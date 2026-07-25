import uvicorn
from fastapi.params import Query
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from models import Base, UserCreateSchema, UserResponseSchema, AdCreateSchema, AdResponseSchema, PetAdModel, ItemAdModel
from core import LostAndFound
from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


app = FastAPI(lifespan=lifespan)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def get_engine(session: AsyncSession = Depends(get_db)):
    yield LostAndFound(session)


@app.post("/register", response_model=UserResponseSchema)
async def register(user_data: UserCreateSchema, engine: LostAndFound = Depends(get_engine)):
    user = await engine.register_user(name=user_data.name, contact_info=user_data.contact_info)

    return user


@app.post("/ads", response_model=AdResponseSchema)
async def create_ad(ad_data: AdCreateSchema, engine: LostAndFound = Depends(get_engine)):
    if ad_data.ad_type == "pet":
        ad = await engine.post_ad_to_user(

            ad_data.user_id,
            PetAdModel,
            category=ad_data.category,
            color=ad_data.color,
            pet_name=ad_data.pet_name,
            breed=ad_data.breed,
            extra_info=ad_data.extra_info

        )
        return ad


    elif ad_data.ad_type == "item":
        ad = await engine.post_ad_to_user(
            ad_data.user_id,
            ItemAdModel,
            category=ad_data.category,
            color=ad_data.color,
            value=ad_data.value,
            extra_info=ad_data.extra_info
        )

        return ad


@app.get("/search", response_model=list[AdResponseSchema])
async def get_filter_ads(
        engine: LostAndFound = Depends(get_engine),
        category: str | None = None,
        color: str | None = None,
        limit: int = Query(default=10, ge=1, le=50),
        offset: int = Query(default=0, ge=0)
):
    return await  engine.filter_ads(category=category, color=color, limit=limit, offset=offset)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
