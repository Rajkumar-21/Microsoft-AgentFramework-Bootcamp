# Agent Registry & Marketplace

A production-ready **Agent Registry** and **Marketplace** for the Microsoft Agent
Framework. Publish, discover, and govern the three building blocks of real-world
agentic apps:

- **Agents** — A2A / OpenAI-compatible / Azure Functions endpoints
- **MCP servers** — Streamable HTTP, stdio, and WebSocket tool servers
- **Skills** — declarative prompt / tool / workflow definitions (YAML)

Agent Framework apps register themselves and **discover** capabilities at runtime
through a typed client SDK, all secured with **Microsoft Entra ID** (OAuth2) and
scoped RBAC.

```
┌──────────────┐   register / discover (OAuth2)   ┌─────────────────────┐
│ AF agents &  │  ─────────────────────────────▶  │  Registry API        │
│ apps (SDK)   │  ◀─────────────────────────────  │  (FastAPI)           │
└──────────────┘        signed JWT (Entra)         │  • Agents            │
        ▲                                          │  • MCP servers       │
        │ browse / publish                         │  • Skills            │
┌──────────────┐                                   │  RBAC: read/publish/ │
│ Marketplace  │  ───────────────────────────────▶ │       manage         │
│ UI (React)   │                                   └─────────┬───────────┘
└──────────────┘                                             │
                                                   ┌─────────▼───────────┐
                                                   │ Azure Cosmos DB      │
                                                   │ (memory fallback for │
                                                   │  local development)  │
                                                   └──────────────────────┘
```

## Why a registry?

Production agent systems are made of many moving parts spread across teams and
orgs. A registry gives you:

- **Discovery** — find the right agent / MCP server / skill without sharing code.
- **Governance** — who published what, which version, who can consume it.
- **Security** — every call is an authenticated, scoped OAuth2 request.
- **Reuse** — an agent pulls approved MCP servers + skills at runtime by name.

## Layout

| Path | What |
|------|------|
| `app/` | FastAPI service (models, security, storage, routers) |
| `app/storage/` | `RegistryStore` protocol + Cosmos DB and in-memory implementations |
| `sdk/` | `registry_client` — AF agents self-register & build tools from the registry |
| `ui/` | React (Vite) marketplace front-end with MSAL sign-in |
| `infra/` | Bicep for Azure Container Apps + Cosmos DB (managed identity) |
| `tests/` | API tests (run fully in-memory, no cloud needed) |

## Quick start (local, no cloud)

```bash
cd agent-registry
python -m venv .venv && .venv\Scripts\activate      # Windows
pip install -e ".[dev]"

# Local dev mode: in-memory store + dev auth (no Entra needed)
copy .env.example .env
uvicorn app.main:app --reload
```

Open <http://localhost:8000/docs> for the OpenAPI explorer. The service seeds a
few sample agents, MCP servers, and skills on startup in dev mode.

## Secure mode (Microsoft Entra ID + Cosmos DB)

Set these in `.env` (see `.env.example` for all options):

```env
REGISTRY_AUTH_MODE=entra
ENTRA_TENANT_ID=<your-tenant-guid>
ENTRA_API_AUDIENCE=api://<registry-app-client-id>
REGISTRY_STORE=cosmos
COSMOS_ENDPOINT=https://<account>.documents.azure.com:443/
# Auth to Cosmos uses DefaultAzureCredential (managed identity in Azure)
```

Scopes / roles enforced by the API:

| Capability | Delegated scope (`scp`) | App role (`roles`) |
|-----------|--------------------------|--------------------|
| Read / discover | `Registry.Read` | `Registry.Agent` |
| Publish / update | `Registry.Publish` | `Registry.Publish` |
| Delete / govern | `Registry.Manage` | `Registry.Manage` |

## Deploy to Azure

```bash
azd up
```

Provisions Azure Container Apps (API), Cosmos DB, and wires **managed identity**
so the service authenticates to Cosmos with **no keys**. See `infra/main.bicep`.
