# 09 – MCP Tools (Model Context Protocol)

!!! abstract "Module Goals"
    Connect agents to external services via MCP — a standard protocol for AI tool integration.

## Key Concepts

| Tool | Managed By | Use Case |
|------|-----------|----------|
| `HostedMCPTool` | Azure AI Foundry | Service-managed MCP servers |
| `MCPStreamableHTTPTool` | Your code | Client-managed MCP servers |

## Code

```python title="modules/09_mcp_tools/main.py"
--8<-- "modules/09_mcp_tools/main.py"
```

## Run It

```bash
uv run python modules/09_mcp_tools/main.py
```

## Exercises

- [ ] Connect to a client-managed MCP server
- [ ] Combine MCP tools with function tools
- [ ] Explore the MCP tool ecosystem

!!! tip "Next"
    [10 – Middleware System](10-middleware-system.md)
