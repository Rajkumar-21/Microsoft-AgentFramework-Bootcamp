"""
Module 18: Memory & Context Management
Session management, chat history, and dynamic context injection.

NOTE: This module demonstrates the concepts. Actual API signatures may vary 
based on the latest agent-framework version. Check the SDK docs for updates.
"""

import asyncio
import os

from agent_framework import AgentSession, InMemoryHistoryProvider
from agent_framework.openai import OpenAIChatClient


async def main():
    chat_client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )

    # Example 1: Session-based memory with InMemoryHistoryProvider
    print("=== Session-Based Memory ===")
    agent = chat_client.as_agent(
        name="MemoryAgent",
        instructions=(
            "You are a personal assistant. Remember all details the user tells you. "
            "When asked to recall information, retrieve it from the conversation."
        ),
        context_providers=[InMemoryHistoryProvider()],
    )

    session = AgentSession()

    # Store information
    await agent.run("My name is Alex and I work at Contoso. My favorite color is blue.", session=session)
    await agent.run("I have a meeting with Sarah tomorrow at 3 PM.", session=session)

    # Retrieve information (agent remembers via InMemoryHistoryProvider + session)
    result = await agent.run("What's my name and when is my meeting?", session=session)
    print(f"Agent: {result.text}\n")

    # Example 2: Dynamic context injection via instructions
    print("=== Dynamic Context Injection ===")

    # Simulate a user profile that gets injected into context
    user_profile = {
        "name": "Rajkumar",
        "role": "Lead Developer",
        "team": "Platform Engineering",
        "preferences": "Prefers concise answers with code examples",
    }

    # Inject context dynamically into instructions
    personalized_agent = chat_client.as_agent(
        name="PersonalizedAgent",
        instructions=(
            f"You are a helpful assistant personalized for the user.\n\n"
            f"User Profile:\n"
            f"- Name: {user_profile['name']}\n"
            f"- Role: {user_profile['role']}\n"
            f"- Team: {user_profile['team']}\n"
            f"- Preferences: {user_profile['preferences']}\n\n"
            f"Tailor your responses to this user's role and preferences."
        ),
    )

    result = await personalized_agent.run("How should I structure my microservices?")
    print(f"Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
