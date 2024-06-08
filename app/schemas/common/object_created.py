from pydantic import BaseModel, ConfigDict, Field


class ObjectCreatedSchema(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    id: str = Field(..., description="ID of created object")
