import asyncio
import sys
import os
import logging
# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.azure_openai_config import get_azure_chat_service
# Validate environment before creating the client
chat_client = get_azure_chat_service()
logging.info(f"Loaded Openai service: {chat_client.endpoint}")

team_agent = chat_client.create_agent(
    name="TeamAgent",
    description="You are helpfull assitant",
    instructions="Always guide user to share team information."
)

main_agent = chat_client.create_agent(
    name="MainAgent",
    description="You are the main assistant",
    instructions="Always guide user to the right resources.",
    tools=[team_agent.as_tool()]  # Using team_agent as a tool
)

async def main():
    result = await main_agent.run("Can I get developer team information?")
    print(result.text)

if __name__ == "__main__":
    asyncio.run(main())