from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_db
from app.repositories.commodity_coin_repository import CommodityCoinRepository
from app.schemas.common.object_created import ObjectCreatedSchema
from app.schemas.flat_coin_schema import CommodityCoinSchema


class CommodityCoinService:
    def __init__(
        self,
        commodity_coin_repository: CommodityCoinRepository,
    ) -> None:
        self.__commodity_coin_repository = commodity_coin_repository

    async def get_commodity_coins(
        self, name: str | None
    ) -> Sequence[CommodityCoinSchema]:
        commodity_coin_models = await self.__commodity_coin_repository.find_all(
            name=name
        )
        return [
            CommodityCoinSchema(
                id=commodity_coin_model.id,
                name=commodity_coin_model.name,
                address=commodity_coin_model.address,
                description=commodity_coin_model.description,
            )
            for commodity_coin_model in commodity_coin_models
        ]

    async def create_commodity_coin(
        self,
        name: str,
        description: str,
    ) -> ObjectCreatedSchema:
        # TODO: Issue a token
        # TODO: Link one to many with commodity coins
        commodity_coin_model = await self.__commodity_coin_repository.create(
            name=name,
            # TODO: Replace with real coin address
            address="",
            description=description,
        )
        return ObjectCreatedSchema(id=commodity_coin_model.id)


async def build_commodity_coin_service(
    session: Annotated[AsyncSession, Depends(get_async_db)]
) -> CommodityCoinService:
    commodity_coin_repository = CommodityCoinRepository(session=session)
    return CommodityCoinService(commodity_coin_repository=commodity_coin_repository)
