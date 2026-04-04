"""
Module 06: Streaming Responses
Real-time response streaming from agents.

Uses agent.run(message, stream=True) which returns a ResponseStream.
Iterate with `async for update in stream` to receive AgentResponseUpdate
chunks, then optionally call `await stream.get_final_response()` for the
complete AgentResponse.
"""

import asyncio
import os

from agent_framework import AgentSession, InMemoryHistoryProvider
from agent_framework.openai import OpenAIChatClient


async def main():
    # --- Azure OpenAI client ---
    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"]
    )

    agent = client.as_agent(
        name="StreamingAgent",
        instructions="You are a storyteller. Tell engaging, detailed stories.",
    )

    # -----------------------------------------------------------------------
    # Example 1: Basic streaming
    # -----------------------------------------------------------------------
    print("=== Streaming Response ===")
    print("Agent: ", end="", flush=True)

    stream = agent.run(
        "Tell me a short story about a robot learning to cook.",
        stream=True,
    )
    async for update in stream:
        if update.text:
            print(update.text, end="", flush=True)
    print("\n")

    # -----------------------------------------------------------------------
    # Example 2: Streaming with session (multi-turn)
    # Uses InMemoryHistoryProvider so the agent remembers prior turns.
    # -----------------------------------------------------------------------
    print("=== Streaming with Session (multi-turn) ===")

    session_agent = client.as_agent(
        name="StreamingStoryAgent",
        instructions="You are a storyteller. Tell engaging, detailed stories.",
        context_providers=[InMemoryHistoryProvider()],
    )
    session = AgentSession()

    print("Agent: ", end="", flush=True)
    stream = session_agent.run(
        "Start a mystery story set in space.",
        stream=True,
        session=session,
    )
    async for update in stream:
        if update.text:
            print(update.text, end="", flush=True)
    # Optionally retrieve the full response after streaming
    final = await stream.get_final_response()
    print(f"\n[Final response length: {len(final.text)} chars]\n")

    print("Agent (continued): ", end="", flush=True)
    stream = session_agent.run(
        "Continue the story with a plot twist.",
        stream=True,
        session=session,
    )
    async for update in stream:
        if update.text:
            print(update.text, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(main())
