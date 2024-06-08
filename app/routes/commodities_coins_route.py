from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query

from app.schemas.create_flat_coin_schema import CreateFlatCoinSchema
from app.schemas.flat_coin_schema import FlatCoinSchema
from app.services.commodity_coin_service import (
    CommodityCoinService,
    build_commodity_coin_service,
)

router = APIRouter(path="")


@router.get("")
async def get_commodity_coins(
    name: Annotated[str, Query()],
    commodity_coin_service: Annotated[
        CommodityCoinService, Depends(build_commodity_coin_service)
    ],
) -> list[FlatCoinSchema]:
    return await commodity_coin_service.get_commodity_coins(name=name)


@router.post("")
async def create_commodity_coin(
    create_flat_coin_schema: Annotated[CreateFlatCoinSchema, Body()],
    commodity_coin_service: Annotated[
        CommodityCoinService, Depends(build_commodity_coin_service)
    ],
) -> list[FlatCoinSchema]:
    return await commodity_coin_service.create_commodity_coin(
        name=create_flat_coin_schema.name,
        create_flat_coin=create_flat_coin_schema.description,
    )
