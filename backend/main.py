from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.analyses import router as analyses_router
from api.actions import router as actions_router
from core.config import settings


def create_app() -> FastAPI:
    api_prefix = f"{settings.API_PREFIX}/{settings.API_VERSION}"

    app = FastAPI(
        title="SerenLexAI API",
        version=settings.API_VERSION,
    )

    # Allow the frontend dev server to talk to the API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(analyses_router, prefix=api_prefix)
    app.include_router(actions_router, prefix=api_prefix)

    return app


app = create_app()

