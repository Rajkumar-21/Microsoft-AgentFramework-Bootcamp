"""Agent Registry integration: discover the warehouse A2A agent + self-register.

Self-contained (httpx). In a real deployment use the registry SDK
(``registry_client.RegistryClient``) instead.
"""

from __future__ import annotations

import logging
import os

import httpx

logger = logging.getLogger("commerce_concierge.registry")


def _headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {os.getenv('REGISTRY_TOKEN', 'dev')}"}


def _base_url() -> str:
    return os.getenv("REGISTRY_BASE_URL", "http://localhost:8000").rstrip("/")


async def discover_warehouse_url() -> str | None:
    """Find a published warehouse agent that speaks A2A."""
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                f"{_base_url()}/agents",
                params={"tag": "warehouse"},
                headers=_headers(),
            )
            resp.raise_for_status()
            for agent in resp.json().get("items", []):
                if agent.get("protocol") == "a2a":
                    return agent["endpoint"]
    except Exception as exc:
        logger.warning("Registry discovery skipped: %s", exc)
    return os.getenv("WAREHOUSE_A2A_URL")


async def self_register() -> None:
    """Advertise this concierge so storefronts can embed it."""
    endpoint = os.getenv("CONCIERGE_ENDPOINT")
    if not endpoint:
        return
    body = {
        "name": "Commerce Concierge",
        "summary": "Retail shopping assistant: find, recommend, quote, escalate.",
        "endpoint": endpoint,
        "protocol": "azure_functions",
        "auth": "entra",
        "scopes": ["Concierge.Invoke"],
        "tags": ["retail", "concierge", "shopping"],
    }
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                f"{_base_url()}/agents", json=body, headers=_headers()
            )
            if resp.status_code in (200, 201):
                logger.info("Registered Commerce Concierge in the registry.")
    except Exception as exc:
        logger.warning("Self-register skipped: %s", exc)
