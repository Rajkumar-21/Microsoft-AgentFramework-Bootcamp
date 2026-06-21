"""Skills catalog: publish and discover reusable prompt/tool/workflow skills."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ..models import (
    Page,
    Publisher,
    ResourceKind,
    Skill,
    SkillCreate,
    SkillUpdate,
)
from ..security import Principal, require_manage, require_publish, require_read
from ..storage.base import RegistryStore
from .deps import get_store

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("", response_model=Page[Skill])
async def list_skills(
    principal: Annotated[Principal, Depends(require_read)],
    store: Annotated[RegistryStore, Depends(get_store)],
    q: str | None = Query(None, description="Free-text search."),
    tag: Annotated[list[str] | None, Query()] = None,
    mine: bool = Query(False),
    offset: int = 0,
    limit: int = Query(50, le=200),
) -> Page[Skill]:
    items, total = await store.list(
        ResourceKind.skill,
        query=q,
        tags=tag,
        publisher_id=principal.id if mine else None,
        visible_to_org=principal.tenant_id,
        offset=offset,
        limit=limit,
    )
    return Page[Skill](items=items, count=len(items), total=total)


@router.get("/{skill_id}", response_model=Skill)
async def get_skill(
    skill_id: str,
    principal: Annotated[Principal, Depends(require_read)],
    store: Annotated[RegistryStore, Depends(get_store)],
) -> Skill:
    skill = await store.get(ResourceKind.skill, skill_id)
    if skill is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Skill not found.")
    return skill  # type: ignore[return-value]


@router.post("", response_model=Skill, status_code=status.HTTP_201_CREATED)
async def publish_skill(
    payload: SkillCreate,
    principal: Annotated[Principal, Depends(require_publish)],
    store: Annotated[RegistryStore, Depends(get_store)],
) -> Skill:
    skill = Skill(
        **payload.model_dump(),
        publisher=Publisher(id=principal.id, name=principal.name),
        partition_key=principal.id,
    )
    return await store.create(skill)  # type: ignore[return-value]


@router.patch("/{skill_id}", response_model=Skill)
async def update_skill(
    skill_id: str,
    payload: SkillUpdate,
    principal: Annotated[Principal, Depends(require_publish)],
    store: Annotated[RegistryStore, Depends(get_store)],
) -> Skill:
    skill = await store.get(ResourceKind.skill, skill_id)
    if skill is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Skill not found.")
    if skill.publisher.id != principal.id and not principal.has("Registry.Manage"):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "Only the publisher can update this skill."
        )
    updated = skill.model_copy(
        update={
            **payload.model_dump(exclude_unset=True),
            "updated_at": datetime.now(timezone.utc),
        }
    )
    return await store.replace(updated)  # type: ignore[return-value]


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(
    skill_id: str,
    principal: Annotated[Principal, Depends(require_manage)],
    store: Annotated[RegistryStore, Depends(get_store)],
) -> None:
    if not await store.delete(ResourceKind.skill, skill_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Skill not found.")
