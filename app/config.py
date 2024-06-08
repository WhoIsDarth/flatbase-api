from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_POOL_SIZE: int
    POSTGRES_MAX_OVERFLOW: int
    POSTGRES_POOL_TIMEOUT: int
    POSTGRES_POOL_RECYCLE: int

    CORS_ORIGINS: list[str]
    CORS_ALLOW_CREDENTIALS: bool
    CORS_ALLOW_METHODS: list[str]
    CORS_ALLOW_HEADERS: list[str]

    LOGGING_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"


settings = Settings()


def pg_dsn(
    host: str,
    db: str,
    port: int,
    username: str,
    password: str,
    schema: str,
) -> str:
    return f"{schema}{username}:{password}@{host}:{port}/{db}"


DB_CONNECTION_STRING = pg_dsn(
    host=settings.POSTGRES_HOST,
    db=settings.POSTGRES_DB,
    port=settings.POSTGRES_PORT,
    username=settings.POSTGRES_USERNAME,
    password=settings.POSTGRES_PASSWORD,
    schema="postgresql://",
)

DB_CONNECTION_STRING_ASYNC = pg_dsn(
    host=settings.POSTGRES_HOST,
    db=settings.POSTGRES_DB,
    port=settings.POSTGRES_PORT,
    username=settings.POSTGRES_USERNAME,
    password=settings.POSTGRES_PASSWORD,
    schema="postgresql+asyncpg://",
)
