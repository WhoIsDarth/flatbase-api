from pydantic import BaseModel, ConfigDict, Field


class CreateCommodityCoinSchema(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    name: str = Field(..., description="Name of coin")
    description: str = Field(..., description="Coin description")