# 01 – Setup & Configuration

!!! abstract "Module Goals"
    Set up your development environment, install dependencies, configure credentials, and validate everything works.

## Key Concepts

| Concept               | Description                                       |
| --------------------- | ------------------------------------------------- |
| `agent-framework`   | Main Python package from PyPI                     |
| `uv`                | Fast Python package manager                       |
| Environment variables | Azure OpenAI / AI Foundry credentials             |
| Authentication        | API key vs Azure Identity (CLI, managed identity) |

## Environment Variables

Create a `.env` file in your project root (or set in your shell):

```bash
# Azure OpenAI (Modules 02–10)
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2025-01-01-preview

# Azure AI Foundry (Modules 08+, hosted agents)
AZURE_AI_PROJECT_ENDPOINT=https://<project>.services.ai.azure.com/api/projects/<id>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o-mini
```

## Installation

```bash
# Create project and install
uv init
uv add agent-framework --prerelease=allow
uv add azure-identity
```

## Code: Configuration Validator

```python
--8<-- "modules/01_setup_and_configuration/main.py"
```

## Run It

```bash
uv run python modules/01_setup_and_configuration/main.py
```

## Exercises

- [ ] Install `agent-framework` using `uv`
- [ ] Create `.env` file with your Azure OpenAI credentials
- [ ] Run the config validator and fix any missing variables
- [ ] Test authentication with `az login` for AzureCliCredential

!!! tip "Next"
    Once your config validates, move on to [02 – Hello Agent](02-hello-agent.md).
