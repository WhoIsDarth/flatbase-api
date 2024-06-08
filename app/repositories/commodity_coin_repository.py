from typing import Sequence

from sqlalchemy import asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.commodity_coin_model import CommodityCoinModel


class CommodityCoinRepository:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.__session = session

    async def find_all(self, name: str | None) -> Sequence[CommodityCoinModel]:
        query = (
            select(CommodityCoinModel)
            .where(CommodityCoinModel.name == name)
            .order_by(asc(CommodityCoinModel.created_at))
        )

        result = await self.__session.execute(query)

        return result.scalars().all()

    async def create(
        self, name: str, address: str, description: str | None
    ) -> CommodityCoinModel:
        new_commodity_coin = CommodityCoinModel(
            name=name, address=address, description=description
        )

        self.__session.add(new_commodity_coin)
        await self.__session.commit()
        await self.__session.refresh(new_commodity_coin)

        return new_commodity_coin
