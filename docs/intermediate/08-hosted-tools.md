# 08 – Hosted Tools

!!! abstract "Module Goals"
    Use Azure-hosted tools: Code Interpreter, File Search, and Web Search.

## Key Concepts

| Tool | Import | Purpose |
|------|--------|---------|
| `HostedCodeInterpreterTool` | `from agent_framework import ...` | Execute Python on Azure |
| `HostedFileSearchTool` | `from agent_framework import ...` | Search vector stores |
| `HostedWebSearchTool` | `from agent_framework import ...` | Bing web search |

!!! warning "Requires AzureAIAgentsProvider"
    Hosted tools only work with `AzureAIAgentsProvider`, not `AzureOpenAIChatClient`.

## Code

```python title="modules/08_hosted_tools/main.py"
--8<-- "modules/08_hosted_tools/main.py"
```

## Run It

```bash
uv run python modules/08_hosted_tools/main.py
```

## Exercises

- [ ] Create an agent with Code Interpreter for math/data tasks
- [ ] Create an agent with Web Search for real-time info
- [ ] Combine Code Interpreter + Web Search

!!! tip "Next"
    [09 – MCP Tools](09-mcp-tools.md)
