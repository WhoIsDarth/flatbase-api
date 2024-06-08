from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.schemas.demo_schema import DemoSchema
from app.services.demo_service import DemoService, build_demo_service

router = APIRouter()


@router.get("/demo")
async def get_demos_by_name_route(
    name: Annotated[str, Query()],
    demo_service: Annotated[DemoService, Depends(build_demo_service)],
) -> list[DemoSchema]:
    return await demo_service.find_all_by_name(name=name)
