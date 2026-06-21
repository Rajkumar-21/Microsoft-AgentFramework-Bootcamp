# Real-World Projects

These are **end-to-end, deployable** reference applications that combine many
bootcamp lessons into one app and integrate with the **Agent Registry &
Marketplace** in [`../agent-registry`](../agent-registry).

Where the numbered `modules/` teach one concept at a time, these projects show
how the concepts come together in production-shaped code.

| Project | Domain | Combined topics | Deploy target |
|---------|--------|-----------------|---------------|
| [ops-copilot](ops-copilot/) | SRE / incident response | Tools · MCP · Middleware · Magentic supervisor · HITL · Memory · Observability · Registry | Azure Functions |
| [commerce-concierge](commerce-concierge/) | Retail shopping | Structured outputs · Hosted tools · Sequential/Concurrent/Handoff workflows · Streaming · A2A · Registry | Azure Functions |

## How they use the registry

Both projects, on startup:

1. **Discover** approved capabilities from the registry — Ops Copilot pulls
   `operations`-tagged MCP servers; Commerce Concierge finds a `warehouse`
   agent to call over A2A.
2. **Self-register** their own endpoint so other teams/storefronts can find and
   reuse them.

The registry enforces Microsoft Entra ID OAuth2 with three scopes
(`Registry.Read` < `Registry.Publish` < `Registry.Manage`), so discovery and
publishing are authenticated and authorized.

## Quick start (any project)

```bash
cd projects/<project>
python -m venv .venv && .venv\Scripts\activate     # Windows
pip install -e .
copy .env.example .env                              # fill in Azure OpenAI + Registry
python -m app.run "your request here"
```

## Deploy

Each project is an `AgentFunctionApp` and ships with `host.json`,
`requirements.txt`, and a `local.settings.json.example`:

```bash
pip install agent-framework-azurefunctions --pre
func azure functionapp publish <your-function-app>
```

Use **managed identity** for Azure OpenAI, Cosmos DB, and the Registry — none of
the projects require secrets in code.
