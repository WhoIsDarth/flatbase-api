from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_db
from app.repositories.flat_coin_repository import FlatCoinRepository
from app.schemas.common.object_created import ObjectCreatedSchema
from app.schemas.flat_coin_schema import FlatCoinSchema


class FlatCoinService:
    def __init__(
        self,
        flat_coin_repository: FlatCoinRepository,
    ) -> None:
        self.__flat_coin_repository = flat_coin_repository

    async def get_flat_coins(self, name: str | None) -> Sequence[FlatCoinSchema]:
        flat_coin_models = await self.__flat_coin_repository.find_all(name=name)
        return [
            FlatCoinSchema(
                id=flat_coin_model.id,
                name=flat_coin_model.name,
                address=flat_coin_model.address,
                description=flat_coin_model.description,
                # TODO: replace with real commodity_coins
                commodity_coins=[],
            )
            for flat_coin_model in flat_coin_models
        ]

    async def create_flat_coin(
        self,
        name: str,
        description: str,
    ) -> ObjectCreatedSchema:
        # TODO: Issue a token
        # TODO: Link one to many with commodity coins
        flat_coin_model = await self.__flat_coin_repository.create(
            name=name,
            # TODO: Replace with real coin address
            address="",
            description=description,
        )
        return ObjectCreatedSchema(id=flat_coin_model.id)


async def build_flat_coin_service(
    session: Annotated[AsyncSession, Depends(get_async_db)]
) -> FlatCoinService:
    flat_coin_repository = FlatCoinRepository(session=session)
    return FlatCoinService(flat_coin_repository=flat_coin_repository)
