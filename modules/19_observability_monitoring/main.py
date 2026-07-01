"""
Module 19: Observability & Monitoring
Track agent performance, tool usage, and diagnostics.
"""

import asyncio
import json
import os
import time
from datetime import datetime, timezone
from typing import Annotated

from pydantic import Field

from agent_framework import AgentContext, AgentMiddleware, function_middleware, tool
from agent_framework.openai import OpenAIChatClient


# Metrics collector
class MetricsCollector:
    """Simple in-memory metrics collector."""

    def __init__(self):
        self.agent_calls = []
        self.tool_calls = []

    def record_agent_call(self, agent_name: str, duration: float, success: bool):
        self.agent_calls.append({
            "agent": agent_name,
            "duration_ms": round(duration * 1000, 2),
            "success": success,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def record_tool_call(self, tool_name: str, args: dict, duration: float):
        self.tool_calls.append({
            "tool": tool_name,
            "args": args,
            "duration_ms": round(duration * 1000, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def print_report(self):
        print("\n📊 Metrics Report")
        print("=" * 50)
        print(f"Agent Calls: {len(self.agent_calls)}")
        for call in self.agent_calls:
            status = "✅" if call["success"] else "❌"
            print(f"  {status} {call['agent']}: {call['duration_ms']}ms")

        print(f"\nTool Calls: {len(self.tool_calls)}")
        for call in self.tool_calls:
            print(f"  🔧 {call['tool']}: {call['duration_ms']}ms | args={call['args']}")


metrics = MetricsCollector()


# Observability middleware (agent-level)
class ObservabilityMiddleware(AgentMiddleware):
    """Tracks all agent interactions with timing and diagnostics."""

    async def process(self, context: AgentContext, call_next) -> None:
        agent_name = context.agent.name
        start = time.time()
        success = True

        try:
            print(f"  📡 [{agent_name}] Processing request...")
            await call_next()
        except Exception as e:
            success = False
            print(f"  ❌ [{agent_name}] Error: {e}")
            raise
        finally:
            duration = time.time() - start
            metrics.record_agent_call(agent_name, duration, success)
            print(f"  ⏱️  [{agent_name}] Completed in {duration*1000:.0f}ms")


# Tool monitoring middleware
@function_middleware
async def tool_monitor(context, call_next):
    """Track tool invocations."""
    tool_name = context.function.name
    args = context.arguments
    start = time.time()

    print(f"  🔧 Tool call: {tool_name}({json.dumps(args)})")
    await call_next()

    duration = time.time() - start
    metrics.record_tool_call(tool_name, args, duration)


# Sample tools
@tool
def get_stock_price(
    symbol: Annotated[str, Field(description="Stock ticker symbol")],
) -> str:
    """Get the current stock price."""
    prices = {"MSFT": 450.25, "AAPL": 198.50, "GOOGL": 175.30}
    price = prices.get(symbol.upper(), 0)
    return f"{symbol}: ${price}"


@tool
def get_market_summary() -> str:
    """Get today's market summary."""
    return "Markets are up 0.5%. Tech sector leading gains."


async def main():
    chat_client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )

    # Agent with observability middleware
    agent = chat_client.as_agent(
        name="StockAdvisor",
        instructions="You are a stock market advisor. Use tools to get prices and market data.",
        tools=[get_stock_price, get_market_summary],
        middleware=[ObservabilityMiddleware(), tool_monitor],
    )

    # Run several queries
    queries = [
        "What's the price of MSFT stock?",
        "Give me a market summary and AAPL price.",
    ]

    for query in queries:
        print(f"\n{'='*50}")
        print(f"User: {query}")
        result = await agent.run(query)
        print(f"Agent: {result.text}")

    # Print metrics report
    metrics.print_report()


if __name__ == "__main__":
    asyncio.run(main())
