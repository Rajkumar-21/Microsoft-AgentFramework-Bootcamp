# Module 01: Setup & Configuration

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
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2025-01-01-preview

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

## Files
- `main.py` - Configuration setup and validation
- `.env.example` - Template for environment variables
