"""
Module 07: Structured Outputs
Get typed, structured responses from agents using Pydantic models.

Pass the Pydantic model via options={"response_format": MyModel} in agent.run().
The parsed object is available on result.value (the raw JSON is on result.text).
"""

import asyncio
import os

from pydantic import BaseModel, ConfigDict

from agent_framework.openai import OpenAIChatClient


# ---------------------------------------------------------------------------
# Define structured output schemas
# ---------------------------------------------------------------------------
class MovieRecommendation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    year: int
    genre: str
    rating: float
    reason: str


class TripPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    destination: str
    duration_days: int
    budget_estimate: str
    highlights: list[str]
    best_season: str
    tips: list[str]


async def main():
    # --- Azure OpenAI client ---
    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"]
    )

    # Example 1: Movie Recommendation
    print("=== Structured Movie Recommendation ===")
    movie_agent = client.as_agent(
        name="MovieAdvisor",
        instructions="Recommend movies based on user preferences. Respond in structured format.",
    )

    result = await movie_agent.run(
        "Recommend a sci-fi movie from the 2020s",
        options={"response_format": MovieRecommendation},
    )
    movie: MovieRecommendation = result.value
    print(f"Title: {movie.title} ({movie.year})")
    print(f"Genre: {movie.genre} | Rating: {movie.rating}")
    print(f"Why: {movie.reason}")

    # Example 2: Trip Plan
    print("\n=== Structured Trip Plan ===")
    trip_agent = client.as_agent(
        name="TripPlanner",
        instructions="Create detailed trip plans. Respond in structured format.",
    )

    result = await trip_agent.run(
        "Plan a 5-day trip to Barcelona, Spain",
        options={"response_format": TripPlan},
    )
    trip: TripPlan = result.value
    print(f"Destination: {trip.destination} ({trip.duration_days} days)")
    print(f"Budget: {trip.budget_estimate}")
    print(f"Best Season: {trip.best_season}")
    print(f"Highlights: {', '.join(trip.highlights)}")
    print(f"Tips: {', '.join(trip.tips)}")


if __name__ == "__main__":
    asyncio.run(main())
