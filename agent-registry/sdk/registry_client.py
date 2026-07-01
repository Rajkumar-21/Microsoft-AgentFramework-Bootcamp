"""Agent Registry client SDK.

A small, dependency-light client that Microsoft Agent Framework apps use to:

* **self-register** their agent endpoint, and
* **discover** approved MCP servers and skills at runtime.

Authentication mirrors the API's two modes:

* ``dev``   — pass ``token="dev"`` (optionally ``"dev Registry.Publish"``).
* ``entra`` — pass an :class:`~azure.core.credentials.TokenCredential`
  (e.g. ``DefaultAzureCredential`` or ``ClientSecretCredential`` for an agent's
  client-credentials flow). The SDK fetches a bearer token for
  ``api://<audience>/.default`` automatically.

Example — an agent registers itself and builds its toolset::

    from agent_framework.azure import AzureOpenAIChatClient
    from azure.identity import DefaultAzureCredential
    from registry_client import RegistryClient

    client = RegistryClient(
        base_url="https://registry.contoso.com",
        credential=DefaultAzureCredential(),
        api_audience="api://registry-client-id",
    )
    await client.register_agent(
        name="Nexus Concierge",
        summary="A2A concierge",
        endpoint="https://nexus.contoso.com/a2a",
        protocol="a2a",
    )
    tools = await client.build_mcp_tools(tag="operations")
    agent = AzureOpenAIChatClient().create_agent(name="Nexus", tools=tools)
"""

from __future__ import annotations

from typing import Any

import httpx

try:  # azure-identity is optional; only needed for entra mode
    from azure.core.credentials import TokenCredential
except Exception:  # pragma: no cover - optional dependency
    TokenCredential = Any  # type: ignore[assignment, misc]


class RegistryClient:
    """Async client for the Agent Registry API."""

    def __init__(
        self,
        base_url: str,
        *,
        token: str | None = None,
        credential: "TokenCredential | None" = None,
        api_audience: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        if not token and not credential:
            raise ValueError("Provide either a dev `token` or an Entra `credential`.")
        if credential and not api_audience:
            raise ValueError("`api_audience` is required when using a credential.")
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._credential = credential
        self._scope = f"{api_audience}/.default" if api_audience else None
        self._client = httpx.AsyncClient(base_url=self._base_url, timeout=timeout)

    # -- lifecycle -------------------------------------------------------- #
    async def __aenter__(self) -> "RegistryClient":
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.close()

    async def close(self) -> None:
        await self._client.aclose()

    # -- auth ------------------------------------------------------------- #
    def _bearer(self) -> str:
        if self._token:
            return self._token
        # Credential token (client-credentials or managed identity).
        access = self._credential.get_token(self._scope)  # type: ignore[union-attr, arg-type]
        return access.token

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._bearer()}"}

    async def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        resp = await self._client.request(
            method, path, headers=self._headers(), **kwargs
        )
        resp.raise_for_status()
        if resp.status_code == 204:
            return None
        return resp.json()

    # -- identity --------------------------------------------------------- #
    async def whoami(self) -> dict[str, Any]:
        return await self._request("GET", "/me")

    # -- agents ----------------------------------------------------------- #
    async def register_agent(
        self,
        *,
        name: str,
        summary: str,
        endpoint: str,
        protocol: str = "a2a",
        auth: str = "entra",
        scopes: list[str] | None = None,
        tags: list[str] | None = None,
        description: str = "",
        version: str = "1.0.0",
        visibility: str = "public",
    ) -> dict[str, Any]:
        body = {
            "name": name,
            "summary": summary,
            "endpoint": endpoint,
            "protocol": protocol,
            "auth": auth,
            "scopes": scopes or [],
            "tags": tags or [],
            "description": description,
            "version": version,
            "visibility": visibility,
        }
        return await self._request("POST", "/agents", json=body)

    async def list_agents(
        self, *, q: str | None = None, tag: str | None = None
    ) -> list[dict[str, Any]]:
        params = _params(q=q, tag=tag)
        return (await self._request("GET", "/agents", params=params))["items"]

    async def get_agent(self, agent_id: str) -> dict[str, Any]:
        return await self._request("GET", f"/agents/{agent_id}")

    # -- mcp servers ------------------------------------------------------ #
    async def list_mcp_servers(
        self, *, q: str | None = None, tag: str | None = None
    ) -> list[dict[str, Any]]:
        params = _params(q=q, tag=tag)
        return (await self._request("GET", "/mcp-servers", params=params))["items"]

    async def register_mcp_server(
        self,
        *,
        name: str,
        summary: str,
        url: str,
        transport: str = "streamable_http",
        auth: str = "entra",
        scopes: list[str] | None = None,
        tags: list[str] | None = None,
        version: str = "1.0.0",
    ) -> dict[str, Any]:
        body = {
            "name": name,
            "summary": summary,
            "url": url,
            "transport": transport,
            "auth": auth,
            "scopes": scopes or [],
            "tags": tags or [],
            "version": version,
        }
        return await self._request("POST", "/mcp-servers", json=body)

    # -- skills ----------------------------------------------------------- #
    async def list_skills(
        self, *, q: str | None = None, tag: str | None = None
    ) -> list[dict[str, Any]]:
        params = _params(q=q, tag=tag)
        return (await self._request("GET", "/skills", params=params))["items"]

    # -- AF integration --------------------------------------------------- #
    async def build_mcp_tools(
        self, *, tag: str | None = None, q: str | None = None
    ) -> list[Any]:
        """Discover MCP servers and return ready-to-use Agent Framework tools.

        Requires ``agent-framework`` to be installed. Each registered
        streamable-HTTP MCP server becomes an ``MCPStreamableHTTPTool`` you can
        pass to ``create_agent(tools=[...])``.
        """
        from agent_framework import MCPStreamableHTTPTool  # lazy import

        servers = await self.list_mcp_servers(tag=tag, q=q)
        tools: list[Any] = []
        for server in servers:
            if server.get("transport") != "streamable_http":
                continue
            tools.append(
                MCPStreamableHTTPTool(name=server["name"], url=server["url"])
            )
        return tools


def _params(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}
