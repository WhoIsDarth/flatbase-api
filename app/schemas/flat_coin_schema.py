from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.commodity_coin_schema import CommodityCoinSchema


class FlatCoinSchema(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    id: UUID = Field(..., description="ID of coin")
    name: str = Field(..., description="Name of coin")
    address: str = Field(..., description="Coin address")
    description: str = Field(..., description="Coin description")
    commodity_coins: list[CommodityCoinSchema] = Field(
        ..., description="Commodity coins basket"
    )
