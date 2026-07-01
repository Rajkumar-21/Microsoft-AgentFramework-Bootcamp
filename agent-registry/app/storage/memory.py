"""In-memory ``RegistryStore`` — for local dev and tests.

Thread-/task-safe for typical single-process use via an asyncio lock. Data is
lost on restart (reseeded by the app lifespan when ``REGISTRY_SEED`` is true).
"""

from __future__ import annotations

import asyncio

from ..models import ResourceKind, Visibility
from .base import StoredResource


class MemoryStore:
    def __init__(self) -> None:
        self._data: dict[ResourceKind, dict[str, StoredResource]] = {
            ResourceKind.agent: {},
            ResourceKind.mcp_server: {},
            ResourceKind.skill: {},
        }
        self._lock = asyncio.Lock()

    async def init(self) -> None:  # nothing to provision
        return None

    async def close(self) -> None:
        return None

    async def create(self, resource: StoredResource) -> StoredResource:
        async with self._lock:
            self._data[resource.kind][resource.id] = resource
        return resource

    async def get(
        self, kind: ResourceKind, resource_id: str
    ) -> StoredResource | None:
        return self._data[kind].get(resource_id)

    async def replace(self, resource: StoredResource) -> StoredResource:
        async with self._lock:
            self._data[resource.kind][resource.id] = resource
        return resource

    async def delete(self, kind: ResourceKind, resource_id: str) -> bool:
        async with self._lock:
            return self._data[kind].pop(resource_id, None) is not None

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
        items = list(self._data[kind].values())

        if publisher_id:
            items = [r for r in items if r.publisher.id == publisher_id]

        if visible_to_org is not None:
            items = [
                r
                for r in items
                if r.visibility == Visibility.public
                or r.publisher.id == visible_to_org
            ]

        if query:
            q = query.lower()
            items = [
                r
                for r in items
                if q in r.name.lower()
                or q in r.summary.lower()
                or q in r.description.lower()
                or any(q in t.lower() for t in r.tags)
            ]

        if tags:
            wanted = {t.lower() for t in tags}
            items = [r for r in items if wanted <= {t.lower() for t in r.tags}]

        items.sort(key=lambda r: r.updated_at, reverse=True)
        total = len(items)
        return items[offset : offset + limit], total
