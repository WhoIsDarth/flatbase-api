from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import BaseModel


class DemoModel(BaseModel):
    __tablename__ = "pairs"

    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
