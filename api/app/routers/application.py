from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from app.routers.lifetime import register_shutdown_event, register_startup_event
from app.routers.router import api_router


def get_app() -> FastAPI:
    app = FastAPI(
        title="api",
        version=metadata.version("api"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    register_startup_event(app)
    register_shutdown_event(app)

    app.include_router(router=api_router, prefix="/api")

    return app