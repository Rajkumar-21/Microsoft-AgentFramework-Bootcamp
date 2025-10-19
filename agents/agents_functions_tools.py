# Copyright (c) Microsoft. All rights reserved.
import os, sys
import asyncio
from datetime import datetime, timezone
from random import randint
from typing import Annotated
# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
#from azure.identity import AzureCliCredential
from pydantic import Field
from config.azure_openai_config import get_azure_chat_service
from dotenv import load_dotenv
load_dotenv()
"""
Azure OpenAI Assistants with Function Tools Example

This sample demonstrates function tool integration with Azure OpenAI Assistants,
showing both agent-level and query-level tool configuration patterns.
"""
chat_client = get_azure_chat_service()

def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."


def get_time() -> str:
    """Get the current UTC time."""
    current_time = datetime.now(timezone.utc)
    return f"The current UTC time is {current_time.strftime('%Y-%m-%d %H:%M:%S')}."


async def tools_on_agent_level() -> None:
    """Example showing tools defined when creating the agent."""
    print("=== Tools Defined on Agent Level ===")

    # Tools are provided when creating the agent
    # The agent can use these tools for any query during its lifetime
    # For authentication, run `az login` command in terminal or replace AzureCliCredential with preferred
    # authentication option.
    agent = chat_client.create_agent(
    name="HelpDeskAgent",
    description="You are helpfull assitant",
    instructions="Always guide user to route it to respective team based on user queries.",
    tools=[get_time, get_weather]
    )

    # First query - agent can use weather tool
    query1 = "What's the weather like in New York?"
    print(f"User: {query1}")
    result1 = await agent.run(messages=query1)
    print(f"Agent: {result1.text}\n")

    # Second query - agent can use time tool
    query2 = "What's the current UTC time?"
    print(f"User: {query2}")
    result2 = await agent.run(messages=query2)
    print(f"Agent: {result2.text}\n")

    #Third query - agent can use both tools if needed
    query3 = "What's the weather in London and what's the current UTC time?"
    print(f"User: {query3}")
    result3 = await agent.run(messages=query3)
    print(f"Agent: {result3.text}\n")


# async def tools_on_run_level() -> None:
#     """Example showing tools passed to the run method."""
#     print("=== Tools Passed to Run Method ===")

#     # Agent created without tools
#     # For authentication, run `az login` command in terminal or replace AzureCliCredential with preferred
#     # authentication option.
#     agent = chat_client.create_agent(
#     name="HelpDeskAgent",
#     description="You are helpfull assitant",
#     instructions="Always guide user to route it to respective team based on user queries.",
#     tools=[get_time, get_weather]
#     )
#     # First query with weather tool
#     query1 = "What's the weather like in Seattle?"
#     print(f"User: {query1}")
#     result1 = await agent.run(messages=query1, tools=[get_weather])  # Tool passed to run method
#     print(f"Agent: {result1}\n")

#     # Second query with time tool
#     query2 = "What's the current UTC time?"
#     print(f"User: {query2}")
#     result2 = await agent.run(query2, tools=[get_time])  # Different tool for this query
#     print(f"Agent: {result2}\n")

#     # Third query with multiple tools
#     query3 = "What's the weather in Chicago and what's the current UTC time?"
#     print(f"User: {query3}")
#     result3 = await agent.run(query3, tools=[get_weather, get_time])  # Multiple tools
#     print(f"Agent: {result3}\n")




async def main() -> None:
    print("=== Azure OpenAI Assistants Chat Client Agent with Function Tools Examples ===\n")

    await tools_on_agent_level()
    # await tools_on_run_level()


if __name__ == "__main__":
    asyncio.run(main())