from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_db
from app.repositories.demo_repository import DemoRepository
from app.schemas.demo_schema import DemoSchema


class DemoService:
    def __init__(
        self,
        demo_repository: DemoRepository,
    ) -> None:
        self.__demo_repository = demo_repository

    async def find_all_by_name(self, name: str) -> Sequence[DemoSchema]:
        demo_models = await self.__demo_repository.find_all_by_name(name=name)
        return [DemoSchema(name=demo_model.name) for demo_model in demo_models]


async def build_demo_service(
    session: Annotated[AsyncSession, Depends(get_async_db)]
) -> DemoService:
    demo_repository = DemoRepository(session=session)
    return DemoService(demo_repository=demo_repository)
