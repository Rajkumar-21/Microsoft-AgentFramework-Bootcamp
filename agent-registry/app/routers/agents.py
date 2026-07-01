"""Agents catalog: publish, discover, update, and remove agent registrations."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ..models import (
    Agent,
    AgentCreate,
    AgentUpdate,
    Page,
    Publisher,
    ResourceKind,
)
from ..security import Principal, require_manage, require_publish, require_read
from ..storage.base import RegistryStore
from .deps import get_store

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("", response_model=Page[Agent])
async def list_agents(
    principal: Annotated[Principal, Depends(require_read)],
    store: Annotated[RegistryStore, Depends(get_store)],
    q: str | None = Query(None, description="Free-text search."),
    tag: Annotated[list[str] | None, Query()] = None,
    mine: bool = Query(False, description="Only resources I published."),
    offset: int = 0,
    limit: int = Query(50, le=200),
) -> Page[Agent]:
    items, total = await store.list(
        ResourceKind.agent,
        query=q,
        tags=tag,
        publisher_id=principal.id if mine else None,
        visible_to_org=principal.tenant_id,
        offset=offset,
        limit=limit,
    )
    return Page[Agent](items=items, count=len(items), total=total)


@router.get("/{agent_id}", response_model=Agent)
async def get_agent(
    agent_id: str,
    principal: Annotated[Principal, Depends(require_read)],
    store: Annotated[RegistryStore, Depends(get_store)],
) -> Agent:
    agent = await store.get(ResourceKind.agent, agent_id)
    if agent is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Agent not found.")
    return agent  # type: ignore[return-value]


@router.post("", response_model=Agent, status_code=status.HTTP_201_CREATED)
async def publish_agent(
    payload: AgentCreate,
    principal: Annotated[Principal, Depends(require_publish)],
    store: Annotated[RegistryStore, Depends(get_store)],
) -> Agent:
    publisher = Publisher(id=principal.id, name=principal.name)
    agent = Agent(
        **payload.model_dump(),
        publisher=publisher,
        partition_key=principal.id,
    )
    return await store.create(agent)  # type: ignore[return-value]


@router.patch("/{agent_id}", response_model=Agent)
async def update_agent(
    agent_id: str,
    payload: AgentUpdate,
    principal: Annotated[Principal, Depends(require_publish)],
    store: Annotated[RegistryStore, Depends(get_store)],
) -> Agent:
    agent = await store.get(ResourceKind.agent, agent_id)
    if agent is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Agent not found.")
    if agent.publisher.id != principal.id and not principal.has("Registry.Manage"):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "Only the publisher can update this agent."
        )
    updated = agent.model_copy(
        update={
            **payload.model_dump(exclude_unset=True),
            "updated_at": datetime.now(timezone.utc),
        }
    )
    return await store.replace(updated)  # type: ignore[return-value]


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: str,
    principal: Annotated[Principal, Depends(require_manage)],
    store: Annotated[RegistryStore, Depends(get_store)],
) -> None:
    if not await store.delete(ResourceKind.agent, agent_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Agent not found.")
