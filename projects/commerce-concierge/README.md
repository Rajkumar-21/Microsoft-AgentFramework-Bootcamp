# Commerce Concierge — Retail Shopping Agent

A customer-facing **retail concierge** that helps shoppers find products, checks
availability, and prepares an order — then hands off to a human agent for
anything it can't safely complete. It demonstrates a different slice of the
framework from Ops Copilot, focused on **conversational workflows and
structured outputs**.

## Topics combined

| Capability | Bootcamp lesson | Used for |
|-----------|-----------------|----------|
| Structured outputs | 07 | Typed `ProductPick` / `OrderDraft` responses |
| Hosted tools | 08 | Web/code interpreter for shipping estimates |
| Sequential workflow | 11 | understand → recommend → quote |
| Handoff workflow | 12 | Escalate to a human-support agent |
| Concurrent fan-out | 13 | Query catalog + reviews + inventory in parallel |
| Streaming responses | 06 | Token-streamed replies to the shopper |
| Agent-to-Agent (A2A) | 21 | Calls the warehouse agent over A2A |
| Deployment | 22 | Hosted with `AgentFunctionApp` |
| **Agent Registry** | — | Discovers skills/agents to assemble the team |

## Architecture

```
 shopper ─▶ Concierge (sequential workflow, streaming)
              ├─ Understand   → structured intent
              ├─ Research (concurrent): catalog ∥ reviews ∥ inventory
              ├─ Recommend    → ProductPick (structured output)
              └─ Quote        → OrderDraft   (hosted tool: shipping)
                    │
                    └─ handoff ─▶ Human Support agent  (when unsure)
                    └─ A2A ─────▶ Warehouse agent       (stock reservation)
```

## Run locally

```bash
cd projects/commerce-concierge
python -m venv .venv && .venv\Scripts\activate
pip install -e .
copy .env.example .env

python -m app.run "I need a waterproof jacket for hiking under $150"
```

## Deploy to Azure Functions

```bash
pip install agent-framework-azurefunctions --pre
func azure functionapp publish commerce-concierge-prod
```

Endpoint: `POST /api/agents/CommerceConcierge/run`. Configure managed identity
for Azure OpenAI and set `APPLICATIONINSIGHTS_CONNECTION_STRING` for traces.

## Registry integration

On startup the concierge discovers a published **warehouse** agent from the
registry and connects to it over A2A; it also self-registers so it can be
embedded in other storefronts. See [app/registry.py](app/registry.py).
