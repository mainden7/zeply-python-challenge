from typing import Any

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from zeply_python_challenge.config import settings
from zeply_python_challenge.wallets.views import wallets_router


def create_app() -> FastAPI:
    """
    Return FastAPI valgrind instance.

    This function is designed to be main entrypoint where app is created
    and bind with all needed plugins, blueprints, etc. Follows an app factory
    pattern

    Returns:
        FastAPI Application
    """
    app_ = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url=f"{settings.API_V1_STR}/docs",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app_.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin) for origin in settings.BACKEND_CORS_ORIGINS
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # blueprints
    app_.include_router(wallets_router, prefix=settings.API_V1_STR)

    @app_.router.get("/")
    async def root() -> Any:
        """Return an application root url placeholder."""
        return {"msg": "Root page"}

    return app_


app = create_app()
