from typing import Sequence

from sqlalchemy import asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.demo_model import DemoModel


class DemoRepository:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.__session = session

    async def find_all_by_name(self, name: str) -> Sequence[DemoModel]:
        query = (
            select(DemoModel)
            .where(DemoModel.name == name)
            .order_by(asc(DemoModel.created_at))
        )

        result = await self.__session.execute(query)

        return result.scalars().all()
