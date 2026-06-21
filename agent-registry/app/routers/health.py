"""Health and identity endpoints."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from .. import __version__
from ..config import Settings, get_settings
from ..models import HealthStatus
from ..security import Principal, get_principal

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthStatus)
async def health(
    settings: Annotated[Settings, Depends(get_settings)],
) -> HealthStatus:
    return HealthStatus(
        status="ok",
        store=settings.store,
        auth_mode=settings.auth_mode,
        version=__version__,
    )


@router.get("/me", response_model=Principal, tags=["auth"])
async def me(principal: Annotated[Principal, Depends(get_principal)]) -> Principal:
    """Echo the verified caller and their effective permissions."""
    return principal
