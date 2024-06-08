from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import BaseModel


class FlatCoinModel(BaseModel):
    __tablename__ = "flat_coins"

    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    address: Mapped[str] = mapped_column(
        String, nullable=False, index=True, unique=True
    )
    description: Mapped[str] = mapped_column(String, nullable=True)
    issuer_wallet_public_key: Mapped[str] = mapped_column(String, nullable=False)
    issuer_wallet_private_key: Mapped[str] = mapped_column(String, nullable=False)
    holder_wallet_public_key: Mapped[str] = mapped_column(String, nullable=False)
    holder_wallet_private_key: Mapped[str] = mapped_column(String, nullable=False)
