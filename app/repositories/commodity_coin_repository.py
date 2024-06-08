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

    async def find_all(self, name: str | None = None) -> Sequence[CommodityCoinModel]:
        query = select(CommodityCoinModel).order_by(asc(CommodityCoinModel.created_at))
        if name is not None:
            query = query.where(CommodityCoinModel.name == name)

        result = await self.__session.execute(query)
        return result.scalars().all()

    async def create(
        self,
        name: str,
        address: str,
        description: str | None,
        issuer_wallet_public_key: str,
        issuer_wallet_private_key: str,
        holder_wallet_public_key: str,
        holder_wallet_private_key: str,
    ) -> CommodityCoinModel:
        new_commodity_coin = CommodityCoinModel(
            name=name,
            address=address,
            description=description,
            issuer_wallet_public_key=issuer_wallet_public_key,
            issuer_wallet_private_key=issuer_wallet_private_key,
            holder_wallet_public_key=holder_wallet_public_key,
            holder_wallet_private_key=holder_wallet_private_key,
        )

        self.__session.add(new_commodity_coin)
        await self.__session.commit()
        await self.__session.refresh(new_commodity_coin)

        return new_commodity_coin
