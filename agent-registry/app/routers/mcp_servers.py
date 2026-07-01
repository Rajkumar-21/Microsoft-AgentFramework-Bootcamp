"""MCP servers catalog: publish and discover tool servers."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ..models import (
    MCPServer,
    MCPServerCreate,
    MCPServerUpdate,
    Page,
    Publisher,
    ResourceKind,
)
from ..security import Principal, require_manage, require_publish, require_read
from ..storage.base import RegistryStore
from .deps import get_store

router = APIRouter(prefix="/mcp-servers", tags=["mcp-servers"])


@router.get("", response_model=Page[MCPServer])
async def list_mcp_servers(
    principal: Annotated[Principal, Depends(require_read)],
    store: Annotated[RegistryStore, Depends(get_store)],
    q: str | None = Query(None, description="Free-text search."),
    tag: Annotated[list[str] | None, Query()] = None,
    mine: bool = Query(False),
    offset: int = 0,
    limit: int = Query(50, le=200),
) -> Page[MCPServer]:
    items, total = await store.list(
        ResourceKind.mcp_server,
        query=q,
        tags=tag,
        publisher_id=principal.id if mine else None,
        visible_to_org=principal.tenant_id,
        offset=offset,
        limit=limit,
    )
    return Page[MCPServer](items=items, count=len(items), total=total)


@router.get("/{server_id}", response_model=MCPServer)
async def get_mcp_server(
    server_id: str,
    principal: Annotated[Principal, Depends(require_read)],
    store: Annotated[RegistryStore, Depends(get_store)],
) -> MCPServer:
    server = await store.get(ResourceKind.mcp_server, server_id)
    if server is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "MCP server not found.")
    return server  # type: ignore[return-value]


@router.post("", response_model=MCPServer, status_code=status.HTTP_201_CREATED)
async def publish_mcp_server(
    payload: MCPServerCreate,
    principal: Annotated[Principal, Depends(require_publish)],
    store: Annotated[RegistryStore, Depends(get_store)],
) -> MCPServer:
    server = MCPServer(
        **payload.model_dump(),
        publisher=Publisher(id=principal.id, name=principal.name),
        partition_key=principal.id,
    )
    return await store.create(server)  # type: ignore[return-value]


@router.patch("/{server_id}", response_model=MCPServer)
async def update_mcp_server(
    server_id: str,
    payload: MCPServerUpdate,
    principal: Annotated[Principal, Depends(require_publish)],
    store: Annotated[RegistryStore, Depends(get_store)],
) -> MCPServer:
    server = await store.get(ResourceKind.mcp_server, server_id)
    if server is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "MCP server not found.")
    if server.publisher.id != principal.id and not principal.has("Registry.Manage"):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "Only the publisher can update this server."
        )
    updated = server.model_copy(
        update={
            **payload.model_dump(exclude_unset=True),
            "updated_at": datetime.now(timezone.utc),
        }
    )
    return await store.replace(updated)  # type: ignore[return-value]


@router.delete("/{server_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mcp_server(
    server_id: str,
    principal: Annotated[Principal, Depends(require_manage)],
    store: Annotated[RegistryStore, Depends(get_store)],
) -> None:
    if not await store.delete(ResourceKind.mcp_server, server_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "MCP server not found.")
