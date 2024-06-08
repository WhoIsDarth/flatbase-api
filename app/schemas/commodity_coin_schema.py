from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CommodityCoinSchema(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    id: UUID = Field(..., description="ID of coin")
    name: str = Field(..., description="Name of coin")
    address: str = Field(..., description="Coin address")
    description: str = Field(..., description="Coin description")
