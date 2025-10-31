# corrected_supervisor.py
import os
import sys
import asyncio
import logging
from datetime import datetime
from typing import Annotated
from pydantic import Field

# Add the project root directory to Python path if needed (your project layout)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Use a proper logger
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

from agent_framework import ChatMessage, ConcurrentBuilder
# Use whatever chat client factory you already have in your project
from config.azure_openai_config import get_azure_chat_service
from dotenv import load_dotenv

load_dotenv()
chat_client = get_azure_chat_service()

# ---------------------------------------------------------------------
# Tools for weekend agent
# ---------------------------------------------------------------------
def get_weather(
    city: Annotated[str, Field(description="The city to get the weather for.")],
    date: Annotated[str, Field(description="The date to get weather for in format YYYY-MM-DD.")],
) -> dict:
    """Returns weather data for a given city and date."""
    logger.info("Tool: get_weather called")
    # Simulate weather data retrieval
    import random
    if random.random() < 0.05:
        return {"temperature": 72, "description": "Sunny"}
    else:
        return {"temperature": 60, "description": "Rainy"}


def get_activities(
    city: Annotated[str, Field(description="The city to get activities for.")],
    date: Annotated[str, Field(description="The date to get activities for in format YYYY-MM-DD.")],
) -> list[dict]:
    """Returns a list of activities for a given city and date."""
    logger.info("Tool: get_activities called")
    return [
        {"name": "Hiking", "location": city},
        {"name": "Beach", "location": city},
        {"name": "Museum", "location": city},
    ]


def get_current_date() -> str:
    """Gets the current date from the system (YYYY-MM-DD)."""
    return datetime.now().strftime("%Y-%m-%d")


# ---------------------------------------------------------------------
# Tools for meal agent
# ---------------------------------------------------------------------
def find_recipes(
    query: Annotated[str, Field(description="User query or desired meal/ingredient")],
) -> list[dict]:
    """Returns recipes (JSON) based on a query."""
    logger.info(f"Tool: find_recipes called with query='{query}'")
    q = (query or "").lower()
    if "pasta" in q:
        return [
            {
                "title": "Pasta Primavera",
                "ingredients": ["pasta", "vegetables", "olive oil"],
                "steps": ["Cook pasta.", "Sauté vegetables."],
            }
        ]
    elif "tofu" in q:
        return [
            {
                "title": "Tofu Stir Fry",
                "ingredients": ["tofu", "soy sauce", "vegetables"],
                "steps": ["Cube tofu.", "Stir fry veggies."],
            }
        ]
    else:
        return [
            {
                "title": "Grilled Cheese Sandwich",
                "ingredients": ["bread", "cheese", "butter"],
                "steps": ["Butter bread.", "Place cheese between slices.", "Grill until golden brown."],
            }
        ]


def check_fridge() -> list[str]:
    """Returns a JSON list of ingredients currently in the fridge."""
    import random
    logger.info("Tool: check_fridge called")
    if random.random() < 0.5:
        return ["pasta", "tomato sauce", "bell peppers", "olive oil"]
    else:
        return ["tofu", "soy sauce", "broccoli", "carrots"]


# ---------------------------------------------------------------------
# Create the two domain agents exactly like before (tools are plain functions)
# ---------------------------------------------------------------------
weekend_agent = chat_client.create_agent(
    name="weekend_agent",
    instructions=(
        "You help users plan their weekends and choose the best activities for the given weather. "
        "If an activity would be unpleasant in the weather, don't suggest it. Include the date of the weekend in your response."
    ),
    tools=[get_weather, get_activities, get_current_date],
)

meal_agent = chat_client.create_agent(
    name="meal_agent",
    instructions=(
        "You help users plan meals and choose the best recipes. Include the ingredients and cooking instructions in your response. "
        "Indicate what the user needs to buy from the store when their fridge is missing ingredients."
    ),
    tools=[find_recipes, check_fridge],
)


# ---------------------------------------------------------------------
# Supervisor orchestration using a Concurrent workflow (fan-out to both agents and aggregate)
# Uses the same pattern as the concurrent_agents sample.
# ---------------------------------------------------------------------
async def run_supervisor(query: str) -> str:
    logger.info("Supervisor: starting workflow for query: %s", query)

    # Build a simple concurrent workflow that fans out the same user prompt to both agents
    workflow = ConcurrentBuilder().participants([weekend_agent, meal_agent]).build()

    events = await workflow.run(query)
    outputs = events.get_outputs()  # list of aggregated ChatMessage lists (one per participant + user message)

    if not outputs:
        return "No response produced."

    # Compose a human-friendly aggregate
    pieces = []
    for output in outputs:
        # `output` is typically a list[ChatMessage] representing the concatenated conversation for that branch
        # Find the last assistant (agent) message in this list
        assistant_texts = []
        for msg in output:
            if getattr(msg, "role", None) == "assistant" or getattr(msg, "author_name", None):
                text = (msg.text or "").strip()
                if text:
                    assistant_texts.append((msg.author_name or "assistant", text))
        if assistant_texts:
            # Use the last assistant entry from this branch
            author, text = assistant_texts[-1]
            pieces.append(f"{author}:\n{text}")

    final = "\n\n---\n\n".join(pieces)
    logger.info("Supervisor: workflow complete")
    return final


async def main_cli():
    # Example CLI-style run
    user_query = "Plan a Saturday: we want outdoor activities and a pasta dinner"
    result = await run_supervisor(user_query)
    print("Supervisor final aggregated response:\n")
    print(result)


if __name__ == "__main__":
    asyncio.run(main_cli())