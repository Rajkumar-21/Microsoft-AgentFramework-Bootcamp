"""
Module 08: Hosted Tools
Use provider-hosted tools: Code Interpreter, Web Search, File Search.

Clients that implement SupportsCodeInterpreterTool / SupportsWebSearchTool
provide factory methods:
  - client.get_code_interpreter_tool()
  - client.get_web_search_tool()

These return tool objects you pass via tools= to as_agent() or Agent().
Both OpenAIChatClient (Azure OpenAI) and FoundryChatClient support them.
"""

import asyncio
import os

from agent_framework.openai import OpenAIChatClient


async def main():
    # --- Azure OpenAI client (Responses API) ---
    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"]
    )

    # -----------------------------------------------------------------------
    # Example 1: Code Interpreter
    # -----------------------------------------------------------------------
    print("=== Code Interpreter ===")
    code_tool = client.get_code_interpreter_tool()
    code_agent = client.as_agent(
        name="CodeAgent",
        instructions="You can execute Python code to solve problems. Always show your work.",
        tools=[code_tool],
    )

    result = await code_agent.run(
        "Calculate the first 20 Fibonacci numbers and find which are also prime."
    )
    print(f"Agent: {result.text}\n")

    # -----------------------------------------------------------------------
    # Example 2: Web Search
    # -----------------------------------------------------------------------
    print("=== Web Search ===")
    web_tool = client.get_web_search_tool()
    search_agent = client.as_agent(
        name="SearchAgent",
        instructions="You can search the web. Provide accurate, up-to-date information.",
        tools=[web_tool],
    )

    result = await search_agent.run(
        "What are the latest developments in Microsoft agent framework latest release version as of april 2026?"
    )
    print(f"Agent: {result.text}\n")

    # -----------------------------------------------------------------------
    # Example 3: Combined tools (Code Interpreter + Web Search)
    # -----------------------------------------------------------------------
    print("=== Combined Tools ===")
    multi_agent = client.as_agent(
        name="ResearchAgent",
        instructions=(
            "You are a research assistant. Search the web for data, "
            "then use code to analyze it."
        ),
        tools=[code_tool, web_tool],
    )

    result = await multi_agent.run(
        "Search for the top 5 programming languages in 2025 and create a bar chart."
    )
    print(f"Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
