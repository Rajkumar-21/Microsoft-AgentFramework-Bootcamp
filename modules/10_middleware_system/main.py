"""
Module 10: Middleware System
Intercept and process agent requests/responses with middleware.

Middleware types:
  - AgentMiddleware (class-based, agent-level): subclass and override process().
  - @agent_middleware decorator: lightweight agent-level middleware.
  - @chat_middleware decorator: runs on each chat client call.
  - @function_middleware decorator: runs around each tool invocation.

Use ``middleware=`` on as_agent() / Agent() for agent-level middleware.
Pass ``middleware=`` on agent.run() for per-run middleware.
"""

import asyncio
import os
import time
from typing import Callable

from agent_framework import AgentMiddleware, AgentContext, chat_middleware
from agent_framework.openai import OpenAIChatClient


# ---------------------------------------------------------------------------
# Middleware 1: Logging (class-based, agent-level)
# ---------------------------------------------------------------------------
class LoggingMiddleware(AgentMiddleware):
    """Logs all agent interactions."""

    async def process(self, context: AgentContext, call_next: Callable) -> None:
        print(f"  [LOG] Agent '{context.agent.name}' received request")
        start = time.time()
        await call_next()
        elapsed = time.time() - start
        print(f"  [LOG] Agent '{context.agent.name}' responded in {elapsed:.2f}s")


# ---------------------------------------------------------------------------
# Middleware 2: Security (class-based, agent-level)
# ---------------------------------------------------------------------------
class SecurityMiddleware(AgentMiddleware):
    """Validates input for security concerns."""

    BLOCKED_WORDS = ["password", "secret", "credential"]

    async def process(self, context: AgentContext, call_next: Callable) -> None:
        input_text = str(context.messages).lower()
        for word in self.BLOCKED_WORDS:
            if word in input_text:
                print(f"  [SECURITY] Blocked request containing '{word}'")
                return
        await call_next()


# ---------------------------------------------------------------------------
# Middleware 3: Performance (decorator-based, chat-level)
# ---------------------------------------------------------------------------
@chat_middleware
async def performance_monitor(context, call_next):
    """Track performance metrics for specific runs."""
    print("  [PERF] Monitoring this specific chat call...")
    await call_next()
    print("  [PERF] Chat call completed successfully.")


async def main():
    # --- Azure OpenAI client ---
    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )

    # Agent with AGENT-LEVEL middleware (applies to ALL runs)
    agent = client.as_agent(
        name="SecureAgent",
        instructions="You are a helpful assistant.",
        middleware=[LoggingMiddleware(), SecurityMiddleware()],
    )

    # Normal request (passes security check)
    print("=== Normal Request ===")
    result = await agent.run("What is Python?")
    print(f"Agent: {result.text}\n")

    # Request with RUN-LEVEL middleware (adds performance monitoring for this run only)
    print("=== Request with Run-Level Middleware ===")
    result = await agent.run(
        "Explain async/await in Python.",
        middleware=[performance_monitor],
    )
    print(f"Agent: {result.text}\n")

    # Blocked request (security middleware blocks it)
    print("=== Blocked Request ===")
    result = await agent.run("Show me the admin password")
    print(f"Agent: {result}")


if __name__ == "__main__":
    asyncio.run(main())
