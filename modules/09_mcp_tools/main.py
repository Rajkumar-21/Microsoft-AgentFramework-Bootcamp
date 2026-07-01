"""
Module 09: MCP Tools (Model Context Protocol)
Connect agents to external services via MCP.

Use MCPStreamableHTTPTool (or MCPStdioTool / MCPWebsocketTool) to interface
with MCP servers.  Wrap the tool in `async with` for proper lifecycle
management, then pass it to as_agent() or Agent() via tools=.
"""

import asyncio
import os

from agent_framework import MCPStreamableHTTPTool
from agent_framework.openai import OpenAIChatClient


async def main():
    # --- Azure OpenAI client ---
    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"]
    )

    # Client-managed MCP tool — wraps an external MCP server endpoint.
    # Use `async with` to manage the connection lifecycle.
    async with MCPStreamableHTTPTool(
        name="DocsMCP",
        url="https://learn.microsoft.com/api/mcp",  # Example MCP endpoint
    ) as mcp_tool:
        # Agent with MCP tool
        agent = client.as_agent(
            name="MCPAgent",
            instructions=(
                "You are a documentation assistant. "
                "Use the MCP tool to search and retrieve documentation."
            ),
            tools=[mcp_tool],
        )

        result = await agent.run(
            "Find documentation about Azure AI Agent Service"
        )
        print(f"Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
