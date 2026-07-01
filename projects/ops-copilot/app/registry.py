"""Agent Registry integration: discover MCP tools and self-register.

Self-contained (httpx) so the project doesn't depend on the registry package
being installed. In a real deployment you'd `pip install` the registry SDK and
use ``registry_client.RegistryClient`` instead.
"""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx

logger = logging.getLogger("ops_copilot.registry")


def _headers() -> dict[str, str]:
    token = os.getenv("REGISTRY_TOKEN", "dev")
    return {"Authorization": f"Bearer {token}"}


def _base_url() -> str:
    return os.getenv("REGISTRY_BASE_URL", "http://localhost:8000").rstrip("/")


async def discover_mcp_tools(tag: str = "operations") -> list[Any]:
    """Fetch approved MCP servers and build Agent Framework MCP tools."""
    try:
        from agent_framework import MCPStreamableHTTPTool
    except ImportError:  # agent-framework not installed in this context
        return []

    tools: list[Any] = []
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                f"{_base_url()}/mcp-servers",
                params={"tag": tag},
                headers=_headers(),
            )
            resp.raise_for_status()
            for server in resp.json().get("items", []):
                if server.get("transport") != "streamable_http":
                    continue
                tools.append(
                    MCPStreamableHTTPTool(name=server["name"], url=server["url"])
                )
    except Exception as exc:  # registry optional — degrade gracefully
        logger.warning("Registry discovery skipped: %s", exc)
    return tools


async def self_register() -> None:
    """Advertise this agent in the registry so other teams can find it."""
    endpoint = os.getenv("OPS_COPILOT_ENDPOINT")
    if not endpoint:
        return
    body = {
        "name": "Ops Copilot",
        "summary": "Incident operations agent (triage, mitigation, comms).",
        "endpoint": endpoint,
        "protocol": "azure_functions",
        "auth": "entra",
        "scopes": ["OpsCopilot.Invoke"],
        "tags": ["operations", "incident", "supervisor"],
    }
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                f"{_base_url()}/agents", json=body, headers=_headers()
            )
            if resp.status_code in (200, 201):
                logger.info("Registered Ops Copilot in the registry.")
            else:
                logger.warning("Self-register returned %s", resp.status_code)
    except Exception as exc:
        logger.warning("Self-register skipped: %s", exc)
