from pydantic import BaseModel, ConfigDict, Field


class DemoSchema(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    name: str = Field(..., description="Name of schema")
