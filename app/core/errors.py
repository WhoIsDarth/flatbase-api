import logging

from fastapi import Request
from fastapi.responses import ORJSONResponse

from app.schemas.common.error import ApiErrorSchema

logger = logging.getLogger(__name__)


class ServiceError(Exception):
    code: int = 500
    reason: str = ""


def service_api_exception_handler(
    request: Request,
    exc: ServiceError,
) -> ORJSONResponse:
    if exc.code >= 500:
        logger.exception(exc)

    content = ApiErrorSchema(
        code=exc.code,
        reason=exc.reason,
    )
    return ORJSONResponse(status_code=exc.code, content=content.model_dump())
