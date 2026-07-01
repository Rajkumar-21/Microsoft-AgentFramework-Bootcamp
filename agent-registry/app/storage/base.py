"""``RegistryStore`` protocol + a factory that selects the backend."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ..config import Settings
from ..models import Agent, MCPServer, ResourceKind, Skill

# A stored document is one of the three concrete resource types.
StoredResource = Agent | MCPServer | Skill


@runtime_checkable
class RegistryStore(Protocol):
    """Backend-agnostic persistence for catalog resources.

    Implementations must be safe to share across requests. All methods are
    async so a single interface covers both in-memory and Cosmos backends.
    """

    async def init(self) -> None:
        """Create databases/containers if needed. Idempotent."""
        ...

    async def close(self) -> None:
        ...

    async def create(self, resource: StoredResource) -> StoredResource:
        ...

    async def get(self, kind: ResourceKind, resource_id: str) -> StoredResource | None:
        ...

    async def replace(self, resource: StoredResource) -> StoredResource:
        ...

    async def delete(self, kind: ResourceKind, resource_id: str) -> bool:
        ...

    async def list(
        self,
        kind: ResourceKind,
        *,
        query: str | None = None,
        tags: list[str] | None = None,
        publisher_id: str | None = None,
        visible_to_org: str | None = None,
        offset: int = 0,
        limit: int = 50,
    ) -> tuple[list[StoredResource], int]:
        """Return ``(items, total)`` matching the filters.

        ``visible_to_org`` includes public resources plus private resources
        whose publisher tenant equals the value (org-scoped visibility).
        """
        ...


def get_store(settings: Settings) -> RegistryStore:
    """Instantiate the configured store. Call ``await store.init()`` after."""
    if settings.store == "cosmos":
        from .cosmos import CosmosStore

        return CosmosStore(settings)
    from .memory import MemoryStore

    return MemoryStore()
