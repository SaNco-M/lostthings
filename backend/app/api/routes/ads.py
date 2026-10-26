from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_ad_service
from app.exceptions import AdNotFoundError
from app.schemas import AnimalAdResponseSchema, AnyAdCreateSchema
from app.service import AdService

router = APIRouter(prefix="/api/ads", tags=["Ads"])


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=AnimalAdResponseSchema
)
async def create_ad(
    data: AnyAdCreateSchema, service: Annotated[AdService, Depends(get_ad_service)]
):
    # Заглушка
    mock_user_id = 1

    return await service.create_ad(user_id=mock_user_id, data=data)


@router.get(
    "/{ad_id}", status_code=status.HTTP_200_OK, response_model=AnimalAdResponseSchema
)
async def get_ad(ad_id: int, service: Annotated[AdService, Depends(get_ad_service)]):
    try:
        return await service.get_ad_by_id(ad_id=ad_id)

    except AdNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "",
    response_model=list[AnimalAdResponseSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_ads(
    service: Annotated[AdService, Depends(get_ad_service)],
    limit: int = 50,
    offset: int = 0,
):
    return await service.get_all_ads(limit=limit, offset=offset)
