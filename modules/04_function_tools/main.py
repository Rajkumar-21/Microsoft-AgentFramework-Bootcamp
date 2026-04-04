"""
Module 04: Function Tools
Create custom tools that agents can call during execution.

Uses the @tool decorator from agent_framework to define function tools.
Tools are passed to as_agent() or Agent() via the tools= parameter.
"""

import asyncio
import os
from datetime import datetime, timezone
from typing import Annotated

from pydantic import Field

from agent_framework import tool
from agent_framework.openai import OpenAIChatClient


# ---------------------------------------------------------------------------
# Tool 1: Weather lookup
# ---------------------------------------------------------------------------
@tool
def get_weather(
    location: Annotated[str, Field(description="City name to get weather for")],
) -> str:
    """Get the current weather for a given location."""
    # In production, call a real weather API
    weather_data = {
        "Seattle": "62°F, Cloudy",
        "New York": "75°F, Sunny",
        "London": "55°F, Rainy",
    }
    return weather_data.get(location, f"Weather data not available for {location}")


# ---------------------------------------------------------------------------
# Tool 2: Current time
# ---------------------------------------------------------------------------
@tool
def get_current_time() -> str:
    """Get the current date and time in UTC."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


# ---------------------------------------------------------------------------
# Tool 3: Calculator
# ---------------------------------------------------------------------------
@tool
def calculate(
    expression: Annotated[str, Field(description="Math expression to evaluate, e.g. '2 + 3 * 4'")],
) -> str:
    """Evaluate a mathematical expression safely."""
    allowed_chars = set("0123456789+-*/().% ")
    if not all(c in allowed_chars for c in expression):
        return "Error: Only basic math operations are allowed."
    try:
        result = eval(expression)  # Safe due to character allowlist above
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error evaluating expression: {e}"


async def main():
    # --- Azure OpenAI via OpenAIChatClient (Responses API) ---
    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"]
    )

    # Create agent with multiple tools via as_agent()
    agent = client.as_agent(
        name="ToolsAgent",
        instructions=(
            "You are a helpful assistant with access to weather, time, and "
            "calculator tools. Use them when appropriate."
        ),
        tools=[get_weather, get_current_time, calculate],
    )

    # Test each tool
    queries = [
        "What's the weather in Seattle?",
        "What time is it right now?",
        "What is 125 * 37 + 99?",
        "What's the weather in London and what time is it?",
    ]

    for query in queries:
        print(f"\nUser: {query}")
        result = await agent.run(query)
        print(f"Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
