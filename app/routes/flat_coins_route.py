from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query

from app.schemas.create_flat_coin_schema import CreateFlatCoinSchema
from app.schemas.flat_coin_schema import FlatCoinSchema
from app.services.flat_coin_service import FlatCoinService, build_flat_coin_service

router = APIRouter(path="")


@router.get("")
async def get_flat_coins(
    name: Annotated[str, Query()],
    flat_coin_service: Annotated[FlatCoinService, Depends(build_flat_coin_service)],
) -> list[FlatCoinSchema]:
    return await flat_coin_service.get_flat_coins(name=name)


@router.post("")
async def create_flat_coin(
    create_flat_coin_schema: Annotated[CreateFlatCoinSchema, Body()],
    flat_coin_service: Annotated[FlatCoinService, Depends(build_flat_coin_service)],
) -> list[FlatCoinSchema]:
    return await flat_coin_service.create_flat_coin(
        name=create_flat_coin_schema.name,
        create_flat_coin=create_flat_coin_schema.description,
    )
