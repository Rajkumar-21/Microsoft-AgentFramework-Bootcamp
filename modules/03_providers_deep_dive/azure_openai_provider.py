"""
Module 03: Provider - OpenAIChatClient (Azure OpenAI)
Client-side agent using Azure OpenAI deployment via the Responses API.
"""

import asyncio
import os

from agent_framework.openai import OpenAIChatClient


async def main():
    # OpenAIChatClient — uses Azure OpenAI Responses API
    # Accepts: model, azure_endpoint, api_key or credential
    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"]
    )

    # .as_agent() is the convenience method to create an Agent from a client
    agent = client.as_agent(
        name="AzureOpenAIAgent",
        instructions="You are a helpful assistant powered by Azure OpenAI.",
    )

    result = await agent.run("Explain what Azure OpenAI is in 2 sentences.")
    print(f"[AzureOpenAI] {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
