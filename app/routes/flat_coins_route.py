from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path, Query

from app.schemas.common.object_created import ObjectCreatedSchema
from app.schemas.create_flat_coin_schema import CreateFlatCoinSchema
from app.schemas.flat_coin_schema import FlatCoinSchema
from app.schemas.send_stable_coin_schema import SendStableCoinSchema
from app.services.flat_coin_service import FlatCoinService, build_flat_coin_service

router = APIRouter()


@router.get("/coins/flat", response_model=list[FlatCoinSchema])
async def get_flat_coins(
    flat_coin_service: Annotated[FlatCoinService, Depends(build_flat_coin_service)],
    name: Annotated[Optional[str], Query()] = None,
) -> list[FlatCoinSchema]:
    return await flat_coin_service.get_flat_coins(name=name)


@router.post("/coins/flat", response_model=ObjectCreatedSchema)
async def create_flat_coin(
    create_flat_coin_schema: Annotated[CreateFlatCoinSchema, Body()],
    flat_coin_service: Annotated[FlatCoinService, Depends(build_flat_coin_service)],
) -> ObjectCreatedSchema:
    return await flat_coin_service.create_flat_coin(
        name=create_flat_coin_schema.name,
        description=create_flat_coin_schema.description,
        amount_of_tokens=create_flat_coin_schema.amount_of_tokens,
        amount_to_issue=create_flat_coin_schema.amount_to_issue,
        commodities_amount=[
            commodities_to_compose.amount
            for commodities_to_compose in create_flat_coin_schema.commodities_to_compose
        ],
        commodities_ids=[
            commodities_to_compose.id
            for commodities_to_compose in create_flat_coin_schema.commodities_to_compose
        ],
    )


@router.post("/coins/flat/{id}/faucet", response_model=ObjectCreatedSchema)
async def send_flat_coin(
    send_stable_coin_schema: Annotated[SendStableCoinSchema, Body()],
    id: Annotated[UUID, Path()],
    flat_coin_service: Annotated[FlatCoinService, Depends(build_flat_coin_service)],
) -> None:
    await flat_coin_service.flat_coin_faucet(
        flat_coin_id=id,
        flat_coin_amount=send_stable_coin_schema.amount,
        destination_address=send_stable_coin_schema.receiver_address,
    )
