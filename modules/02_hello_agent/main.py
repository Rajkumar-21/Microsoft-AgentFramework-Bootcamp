"""
Module 02: Hello Agent
Your first agent using Microsoft Agent Framework.

Demonstrates:
- OpenAIChatClient for Azure OpenAI (Responses API)
- Agent creation via .as_agent() convenience method
- Running an agent and reading the response
"""

import asyncio
import os

from agent_framework.openai import OpenAIChatClient


async def main():
    # Step 1: Create a chat client pointing to Azure OpenAI
    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"]
    )

    # Step 2: Create an agent using the convenience method
    agent = client.as_agent(
        name="HelloAgent",
        instructions="You are a friendly assistant. Keep responses brief and helpful.",
    )

    # Step 3: Run the agent with a user message
    result = await agent.run("Hello! What is the Microsoft Agent Framework used for agent developments?")

    # Step 4: Print the response
    print(f"Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
