# Module 09: MCP Tools (Model Context Protocol)

## Learning Objectives
- Understand MCP (Model Context Protocol) for external tool integration
- Use `HostedMCPTool` for service-managed MCP servers
- Use `MCPStreamableHTTPTool` for client-managed MCP servers
- Connect agents to external APIs and services via MCP

## Key Concepts
- **MCP** - Standard protocol for connecting AI models to external tools/data
- **`HostedMCPTool`** - MCP server managed by Azure AI Foundry service
- **`MCPStreamableHTTPTool`** - MCP server managed by client (your code)
- **Context managers** - MCP tools require `async with` for lifecycle

## Exercises
1. Create an agent with a client-managed MCP tool
2. Create an agent with a hosted MCP tool
3. Combine MCP tools with function tools and hosted tools

## Files
- `main.py` - MCP tool integration examples
