# :books: Reference

Quick reference for the Microsoft Agent Framework Python SDK.

## Core Imports

```python
# Agents
from agent_framework import Agent, AgentTool

# Providers
from agent_framework import AzureOpenAIChatClient
from agent_framework import AzureAIAgentsProvider

# Tools
from agent_framework import FunctionTool, HostedCodeInterpreterTool
from agent_framework import HostedWebSearchTool, HostedFileSearchTool
from agent_framework import HostedMCPTool, MCPStreamableHTTPTool

# Middleware
from agent_framework import chat_middleware, function_middleware

# Workflows
from agent_framework import WorkflowBuilder, ConcurrentBuilder

# Memory
from agent_framework import InMemoryMemoryProvider

# Auth
from azure.identity import AzureCliCredential, DefaultAzureCredential
```

## Common Patterns

### Create & Run an Agent

```python
agent = Agent(
    name="MyAgent",
    instructions="You are a helpful assistant.",
    model=client,                    # Provider instance
    tools=[my_tool],                 # List of tools
    response_format=MyModel,         # Optional Pydantic model
)
result = await agent.run("Hello!")
print(result.text)
```

### Define a Function Tool

```python
@FunctionTool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Sunny in {city}"
```

### Build a Sequential Workflow

```python
wf = (WorkflowBuilder()
    .set_start_executor(agent_a)
    .add_edge(agent_a, agent_b)
    .build())
result = await wf.run("input")
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL |
| `AZURE_OPENAI_DEPLOYMENT` | Model deployment name |
| `AZURE_OPENAI_API_VERSION` | API version (e.g. `2025-01-01`) |
| `PROJECT_ENDPOINT` | Azure AI Foundry project endpoint |
| `MODEL_DEPLOYMENT` | Foundry model deployment name |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | App Insights connection |

## Links

- [Agent Framework GitHub](https://github.com/microsoft/agent-framework)
- [Azure AI Foundry](https://ai.azure.com)
- [Azure OpenAI Docs](https://learn.microsoft.com/azure/ai-services/openai/)
