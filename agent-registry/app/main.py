"""FastAPI application factory for the Agent Registry & Marketplace."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import __version__
from .config import get_settings
from .routers import agents, health, mcp_servers, skills
from .seed import seed_catalog
from .storage.base import get_store

logger = logging.getLogger("agent_registry")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    store = get_store(settings)
    await store.init()
    app.state.store = store

    if settings.auth_mode == "dev":
        logger.warning(
            "Running with REGISTRY_AUTH_MODE=dev — tokens are NOT verified. "
            "Do not use this in shared or production environments."
        )
    if settings.seed and settings.store == "memory":
        await seed_catalog(store)
        logger.info("Seeded sample catalog data (memory store).")

    try:
        yield
    finally:
        await store.close()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Agent Registry & Marketplace",
        version=__version__,
        description=(
            "Publish, discover, and govern Agents, MCP servers, and Skills for "
            "Microsoft Agent Framework applications. Secured with Microsoft "
            "Entra ID (OAuth2) and scoped RBAC."
        ),
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(agents.router)
    app.include_router(mcp_servers.router)
    app.include_router(skills.router)
    return app


app = create_app()
