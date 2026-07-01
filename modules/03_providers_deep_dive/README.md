# Module 03: Providers Deep Dive

> **Scenario — Northwind IT Service Desk triage.** The *same* triage agent runs
> unchanged on **Azure OpenAI** and **Azure AI Foundry** — only the client construction
> differs. This proves the framework's provider portability and shows keyless auth.

## Learning Objectives
- Understand the three main providers: AzureOpenAI, OpenAI, AzureAIAgentsProvider
- Learn when to use each provider
- Understand the difference between ChatClient-based and hosted agents
- Configure authentication for each provider type

## Key Concepts
- **`AzureOpenAIChatClient`** - Azure OpenAI (your own deployment, client-side)
- **`OpenAIChatClient`** - OpenAI API (direct OpenAI access)
- **`AzureAIAgentsProvider`** - Azure AI Foundry (server-side persistent agents)
- **Context managers** for provider lifecycle (`async with provider:`)

## Provider Comparison

| Provider | Persistence | Tools | Auth | Use Case |
|----------|------------|-------|------|----------|
| AzureOpenAIChatClient | Client-side | Functions only | API Key | Simple agents |
| OpenAIChatClient | Client-side | Functions only | API Key | OpenAI models |
| AzureAIAgentsProvider | Server-side | Functions + Hosted + MCP | Azure Identity | Production agents |

## Exercises
1. Create agents with AzureOpenAIChatClient
2. Create agents with AzureAIAgentsProvider
3. Compare response behavior between providers
4. Experiment with different model deployments

## How to Run
```bash
cd modules/03_providers_deep_dive
python azure_openai_provider.py   # Azure OpenAI (API key or AzureCliCredential)
python azure_ai_provider.py      # Azure AI Foundry (AzureCliCredential; az login first)
```

## Files
- `azure_openai_provider.py` - Triage agent on `AzureOpenAIChatClient`
- `azure_ai_provider.py` - Same triage agent on `AzureAIAgentClient` (Foundry)
