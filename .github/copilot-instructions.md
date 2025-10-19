# Copilot Instructions for Agent Framework Samples

## Project Overview
This repository demonstrates Microsoft Agent Framework usage patterns with Azure OpenAI integration. The framework provides high-level abstractions for building conversational AI agents with tool integration capabilities.

## Architecture & Key Components

### Core Structure
- **`agents/`** - Agent implementations with different patterns
- **`config/`** - Azure OpenAI service configuration and environment management
- **`tools/functions/`** - Reusable function tools for agent capabilities
- **`tools/mcp/`** - Model Context Protocol tools (currently empty)

### Agent Patterns
The codebase demonstrates two primary agent creation patterns:

1. **Basic Agent** (`azure_openai_basic.py`):
   ```python
   agent = chat_client.create_agent(
       name="HelpDeskAgent",
       description="You are helpfull assitant",
       instructions="Always guide user to route it to respective team based on user queries."
   )
   ```

2. **Function Tools Agent** (`agents_functions_tools.py`):
   - Tools defined at agent level (persistent across all queries)
   - Tools passed to `run()` method (query-specific)
   - Mixed approach combining both patterns

### Configuration Pattern
All Azure OpenAI configuration is centralized in `config/azure_openai_config.py`:
- Uses environment variables loaded via `python-dotenv`
- Single `get_azure_chat_service()` factory function
- Required environment variables: `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT_NAME`, `AZURE_OPENAI_API_VERSION`

## Development Workflows

### Setup & Environment
1. **Environment Setup**: Copy `.env.example` to `.env` and configure Azure OpenAI credentials
2. **Dependencies**: Uses `uv` for dependency management with `agent-framework>=1.0.0b251016`
3. **Python Path**: All agent files add project root to `sys.path` for config imports

### Running Agents
```powershell
# Basic conversational agent
uv run .\agents\azure_openai_basic.py

# Function tools demonstration
uv run .\agents\agents_functions_tools.py
```

### Function Tool Development
- Place reusable functions in `tools/functions/`
- Use type annotations and Pydantic `Field` for parameter descriptions
- Example pattern from `time.py`:
  ```python
  def get_time() -> str:
      """Get the current UTC time."""
      # Implementation
  ```

## Project-Specific Conventions

### Import Pattern
All agent files use this sys.path modification:
```python
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### Agent Lifecycle
- **Threading**: All agents support conversation threading via `agent.get_new_thread()`
- **Async Context**: Use `async with ChatAgent()` for proper resource cleanup
- **Streaming**: Results accessed via `result.text` property

### Error Handling
- **Connection Errors**: Usually indicate missing/incorrect `.env` configuration
- **Authentication**: Ensure Azure OpenAI credentials are valid and endpoint is accessible

## Integration Points

### Azure OpenAI Dependencies
- Requires valid Azure OpenAI resource with deployed model
- API version compatibility with `agent-framework` library
- Endpoint must be accessible from development environment

### Tool Integration
- Functions automatically converted to agent tools via framework
- Support for both synchronous and asynchronous tool functions
- Type hints and docstrings used for tool schema generation

## Common Patterns

### Agent Creation with Tools
```python
# Tools at agent level (persistent)
agent = chat_client.create_agent(
    name="AgentName",
    instructions="...",
    tools=[function1, function2]
)

# Tools at run level (per-query)
result = await agent.run(query, tools=[function3])
```

### Configuration Access
Always import and use the centralized config:
```python
from config.azure_openai_config import get_azure_chat_service
chat_client = get_azure_chat_service()
```