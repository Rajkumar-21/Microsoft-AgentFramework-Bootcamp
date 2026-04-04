"""
Module 03: Provider - FoundryChatClient (Azure AI Foundry)
Create agents backed by Azure AI Foundry project deployments.
"""

import asyncio
import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity.aio import AzureCliCredential


async def main():
    # FoundryChatClient — connect to a model deployed in Azure AI Foundry
    # Uses AzureCliCredential for local dev (az login first)
    async with AzureCliCredential() as credential:
        client = FoundryChatClient(
            project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
            model=os.environ["FOUNDRY_MODEL"],
            credential=credential,
        )

        # Option A: Convenience method
        agent = client.as_agent(
            name="FoundryAgent",
            instructions="You are a helpful assistant powered by Azure AI Foundry.",
        )

        result = await agent.run("Explain what Azure AI Foundry is in 2 sentences.")
        print(f"[Foundry .as_agent()] {result.text}")

        # Option B: Explicit Agent constructor
        agent2 = Agent(
            client=client,
            name="FoundryAgent2",
            instructions="You are a concise assistant.",
        )

        result2 = await agent2.run("What is the Microsoft Agent Framework?")
        print(f"[Foundry Agent()] {result2.text}")


if __name__ == "__main__":
    asyncio.run(main())
