from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CommoditiesToCompose(BaseModel):
    amount: float
    id: UUID


class CreateFlatCoinSchema(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    name: str = Field(..., description="Name of coin")
    description: str = Field(..., description="Coin description")
    amount_of_tokens: int = Field(..., description="Coin tokens amount")
    amount_to_issue: int = Field(..., description="Coin tokens amount to issue")
    commodities_to_compose: list[CommoditiesToCompose] = Field(
        ..., description="Commodities to compose"
    )
