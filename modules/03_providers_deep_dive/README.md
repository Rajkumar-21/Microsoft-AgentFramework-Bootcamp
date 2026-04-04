# Module 03: Providers Deep Dive

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

## Files
- `azure_openai_provider.py` - AzureOpenAIChatClient example
- `azure_ai_provider.py` - AzureAIAgentsProvider example
