from pydantic import BaseModel, ConfigDict, Field


class ApiErrorSchema(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    code: int = Field(..., description="Error code")
    reason: str = Field(..., description="Reason of the error")
