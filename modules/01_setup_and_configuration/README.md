# Module 01: Setup & Configuration

> **Scenario — "Atlas" platform readiness check.** A production-style, dependency-free
> validator that gates workstations and CI runners before anyone writes an agent.
> It checks the Python runtime, the `agent-framework` package, and Azure credentials,
> then exits `0` (ready) or `1` (blocked).

## Learning Objectives
- Set up Python environment with `uv` and `agent-framework`
- Configure Azure OpenAI and Azure AI Foundry credentials
- Understand authentication methods (API key, AzureCliCredential, DefaultAzureCredential)
- Validate configuration before running agents

## Key Concepts
- **`agent-framework`** package (PyPI, pre-release)
- **Environment variables**: endpoints, API keys, deployment names
- **Authentication**: API key vs Azure Identity (managed identity, CLI credential)

## Environment Variables Required
```bash
# Azure OpenAI (for Modules 02-10)
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o

# Azure AI Foundry (for hosted agents)
AZURE_AI_PROJECT_ENDPOINT=https://<project>.services.ai.azure.com/api/projects/<id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o-mini

# Optional
OPENAI_API_KEY=<your-openai-key>
BING_CONNECTION_ID=<bing-connection-id>
```

## Exercises
1. Install `agent-framework` using `uv`
2. Create `.env` file with your Azure OpenAI credentials
3. Write a config validation script
4. Test authentication with AzureCliCredential

## How to Run
```bash
cd modules/01_setup_and_configuration
python main.py   # exit 0 = ready, exit 1 = blocked
```

## Files
- `main.py` - Readiness validator (safe to run in CI; never calls a model)
