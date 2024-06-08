from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ObjectCreatedSchema(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    id: UUID = Field(..., description="ID of created object")
