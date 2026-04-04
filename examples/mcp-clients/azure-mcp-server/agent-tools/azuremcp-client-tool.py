"""
import asyncio
from agent_framework import Agent, MCPStdioTool
from agent_framework.openai import OpenAIChatClient

async def local_mcp_example():
    async with (
        MCPStdioTool(
            name="calculator",
            command="uvx",
            args=["mcp-server-calculator"]
        ) as mcp_server,
        Agent(
            client=OpenAIChatClient(),
            name="MathAgent",
            instructions="You are a helpful math assistant that can solve calculations.",
        ) as agent,
    ):
        result = await agent.run(
            "What is 15 * 23 + 45?",
            tools=mcp_server
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(local_mcp_example())
"""
# azure mcp server
import asyncio
from agent_framework import Agent, MCPStdioTool
from agent_framework.openai import OpenAIChatClient

async def azure_mcp_server():
    async with (
        MCPStdioTool(
            name="azure-mcp-server",
            # azure mcp server
            command="uvx",
        ) as mcp_server,
        Agent(
            client=OpenAIChatClient(),
            name="MathAgent",
            instructions="You are a helpful math assistant that can solve calculations.",
        ) as agent,
    ):
        result = await agent.run(
            "What is 15 * 23 + 45?",
            tools=mcp_server
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(azure_mcp_server())