"""
Module 05: Conversation Threads
Multi-turn conversations with persistent context.

Uses InMemoryHistoryProvider (a ContextProvider) to maintain conversation
history between run() calls.  Each call is tied to the same AgentSession
so the agent remembers prior turns.
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

    # Create agent with InMemoryHistoryProvider for conversation memory
    agent = client.as_agent(
        name="ChatBot",
        instructions="You are a helpful travel advisor. Remember all details from the conversation.",
        context_providers=[InMemoryHistoryProvider()],
    )

    # Create a session to tie multiple run() calls together
    session = AgentSession()
    print(f"Session ID: {session.session_id}\n")

    # Multi-turn conversation
    conversation = [
        "I'm planning a trip to Japan for 2 weeks in April.",
        "What are the must-see places in Tokyo?",
        "How about day trips from Tokyo?",
        "Can you summarize my trip plan so far?",
    ]

    for message in conversation:
        print(f"User: {message}")
        result = await agent.run(message, session=session)
        print(f"Agent: {result.text}\n")
        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(main())
