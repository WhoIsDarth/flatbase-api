from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import BaseModel


class CommodityCoinModel(BaseModel):
    __tablename__ = "commodity_coins"

    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    address: Mapped[str] = mapped_column(
        String, nullable=False, index=True, unique=True
    )
    description: Mapped[str] = mapped_column(String, nullable=True)
