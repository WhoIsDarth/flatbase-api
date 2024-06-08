from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.config import settings
from app.core.errors import ServiceError, service_api_exception_handler
from app.routes import demo_route

BASE_PATH = "/api/v1"

app = FastAPI(
    title="Demo FastAPI Service",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    default_response_class=ORJSONResponse,
)

app.exception_handler(ServiceError)(service_api_exception_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Routers
app.include_router(
    demo_route.router,
    prefix=BASE_PATH,
    tags=["demo"],
)
