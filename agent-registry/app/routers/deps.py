"""Shared FastAPI dependencies for routers."""

from __future__ import annotations

from fastapi import Request

from ..storage.base import RegistryStore


def get_store(request: Request) -> RegistryStore:
    """Return the store initialized during app startup."""
    return request.app.state.store
