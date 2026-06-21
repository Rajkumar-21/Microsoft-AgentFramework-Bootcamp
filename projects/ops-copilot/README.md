# Ops Copilot — Incident Operations Agent

A **production-ready, multi-capability** agent that runs an incident-response
workflow for an SRE/operations team. It is the kind of real-world app the
bootcamp lessons build toward, combining many topics into one deployable
service.

## Topics combined

| Capability | Bootcamp lesson | Used for |
|-----------|-----------------|----------|
| Function tools | 04 | Pull metrics, look up runbooks |
| MCP tools | 09 | Paging / ticketing via an MCP server |
| Middleware | 10 | Audit logging + PII redaction on every call |
| Magentic supervisor | 15 | Orchestrates triage → mitigation → comms |
| Human-in-the-loop | 17 | Approval gate before any production action |
| Memory & context | 18 | Remembers the incident timeline across turns |
| Observability | 19 | OpenTelemetry traces to Azure Monitor |
| Deployment | 22 | Hosted with `AgentFunctionApp` on Azure Functions |
| **Agent Registry** | — | Discovers approved MCP servers at runtime + self-registers |

## Architecture

```
        ┌───────────────── Ops Copilot (AgentFunctionApp) ─────────────────┐
        │                                                                  │
 alert ─┤  Magentic manager                                                │
        │   ├─ Triage agent     (function tools: metrics, runbooks)        │
        │   ├─ Mitigation agent (MCP tools from Registry, HITL approval)   │
        │   └─ Comms agent      (drafts status updates)                    │
        │                                                                  │
        │  middleware: audit + redaction   memory: incident timeline       │
        └──────────────┬───────────────────────────────┬──────────────────┘
                       │ discover MCP tools             │ OTel traces
                ┌──────▼───────┐                 ┌──────▼───────┐
                │ Agent Registry│                 │ Azure Monitor │
                └──────────────┘                 └──────────────┘
```

## Run locally

```bash
cd projects/ops-copilot
python -m venv .venv && .venv\Scripts\activate
pip install -e .
copy .env.example .env        # fill in Azure OpenAI + Registry settings

# Run the workflow once from the CLI (no Functions host needed):
python -m app.run "CPU on web-prod-3 is at 98% for 10 minutes"
```

## Deploy to Azure Functions

```bash
# Requires Azure Functions Core Tools v4
pip install agent-framework-azurefunctions --pre
func azure functionapp publish ops-copilot-prod
```

The function exposes `POST /api/agents/OpsCopilot/run`. Configure
**managed identity** for Azure OpenAI and the Registry (no keys), and set
`APPLICATIONINSIGHTS_CONNECTION_STRING` so traces flow to Azure Monitor.

## How registry discovery works

On startup the app calls the Agent Registry to fetch approved MCP servers
tagged `operations`, turns them into `MCPStreamableHTTPTool`s, and gives them to
the mitigation agent. It also self-registers its own endpoint so other teams can
discover it. See [app/registry.py](app/registry.py).
