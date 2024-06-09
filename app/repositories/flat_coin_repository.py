from typing import Sequence
from uuid import UUID

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
        query = select(FlatCoinModel).order_by(asc(FlatCoinModel.created_at))
        if name is not None:
            query = query.where(FlatCoinModel.name == name)

        result = await self.__session.execute(query)
        return result.scalars().all()

    async def find_by_id(self, id: UUID) -> FlatCoinModel | None:
        query = select(FlatCoinModel).where(FlatCoinModel.id == id)
        result = await self.__session.execute(query)
        return result.scalar_one_or_none()

    async def create(
        self,
        name: str,
        address: str,
        description: str | None,
        issuer_wallet_public_key: str,
        issuer_wallet_private_key: str,
        holder_wallet_public_key: str,
        holder_wallet_private_key: str,
    ) -> FlatCoinModel:
        new_flat_coin = FlatCoinModel(
            name=name,
            address=address,
            description=description,
            issuer_wallet_public_key=issuer_wallet_public_key,
            issuer_wallet_private_key=issuer_wallet_private_key,
            holder_wallet_public_key=holder_wallet_public_key,
            holder_wallet_private_key=holder_wallet_private_key,
        )

        self.__session.add(new_flat_coin)
        await self.__session.commit()
        await self.__session.refresh(new_flat_coin)

        return new_flat_coin
