from typing import Sequence

from sqlalchemy import asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.flat_coin_model import FlatCoinModel


class FlatCoinRepository:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.__session = session

    async def find_all(self, name: str | None) -> Sequence[FlatCoinModel]:
        query = (
            select(FlatCoinModel)
            .where(FlatCoinModel.name == name)
            .order_by(asc(FlatCoinModel.created_at))
        )

        result = await self.__session.execute(query)

        return result.scalars().all()

    async def create(
        self, name: str, address: str, description: str | None
    ) -> FlatCoinModel:
        new_flat_coin = FlatCoinModel(
            name=name, address=address, description=description
        )

        self.__session.add(new_flat_coin)
        await self.__session.commit()
        await self.__session.refresh(new_flat_coin)

        return new_flat_coin
