from fastapi import APIRouter, Depends, Query

from backend.app.core import LostAndFound
from backend.app.models import AdCreateSchema, AdResponseSchema, ItemAdModel, PetAdModel

router = APIRouter(tags=["ad"])


@router.post("/ads", response_model=AdResponseSchema)
async def create_ad(
    ad_data: AdCreateSchema, engine: LostAndFound = Depends(get_engine)
):
    if ad_data.ad_type == "pet":
        ad = await engine.post_ad_to_user(
            ad_data.user_id,
            PetAdModel,
            category=ad_data.category,
            color=ad_data.color,
            pet_name=ad_data.pet_name,
            breed=ad_data.breed,
            extra_info=ad_data.extra_info,
        )
        return ad

    elif ad_data.ad_type == "item":
        ad = await engine.post_ad_to_user(
            ad_data.user_id,
            ItemAdModel,
            category=ad_data.category,
            color=ad_data.color,
            value=ad_data.value,
            extra_info=ad_data.extra_info,
        )

        return ad


# @router.get("/search", response_model=list[AdResponseSchema])
# async def get_filter_ads(
#     engine: LostAndFound = Depends(get_engine),
#     category: str | None = None,
#     color: str | None = None,
#     limit: int = Query(default=10, ge=1, le=50),
#     offset: int = Query(default=0, ge=0),
# ):
#     return await engine.filter_ads(
#         category=category, color=color, limit=limit, offset=offset
#     )
