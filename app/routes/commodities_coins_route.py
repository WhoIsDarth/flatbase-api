from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, Query

from app.schemas.commodity_coin_schema import CommodityCoinSchema
from app.schemas.common.object_created import ObjectCreatedSchema
from app.schemas.create_commodity_coin_schema import CreateCommodityCoinSchema
from app.services.commodity_coin_service import (
    CommodityCoinService,
    build_commodity_coin_service,
)

router = APIRouter()


@router.get("/coins/commodity")
async def get_commodity_coins(
    commodity_coin_service: Annotated[
        CommodityCoinService, Depends(build_commodity_coin_service)
    ],
    name: Annotated[Optional[str], Query()] = None,
) -> list[CommodityCoinSchema]:
    return await commodity_coin_service.get_commodity_coins(name=name)


@router.post("/coins/commodity")
async def create_commodity_coin(
    create_commodity_coin_schema: Annotated[CreateCommodityCoinSchema, Body()],
    commodity_coin_service: Annotated[
        CommodityCoinService, Depends(build_commodity_coin_service)
    ],
) -> ObjectCreatedSchema:
    return await commodity_coin_service.create_commodity_coin(
        name=create_commodity_coin_schema.name,
        description=create_commodity_coin_schema.description,
        amount_of_tokens=create_commodity_coin_schema.amount_of_tokens,
        amount_to_issue=create_commodity_coin_schema.amount_to_issue,
    )
