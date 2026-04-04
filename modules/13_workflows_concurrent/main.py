"""
Module 13: Workflows — Concurrent
Run multiple agents in parallel for faster processing.

ConcurrentBuilder(participants=[a, b, c]).build() sends the same input to
every participant simultaneously.  Use with_aggregator() to optionally
combine the parallel outputs.
"""

import asyncio
import os

from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import ConcurrentBuilder


async def main():
    # --- Azure OpenAI client ---
    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )

    # Create specialist agents that run in parallel
    tech_researcher = client.as_agent(
        name="TechResearcher",
        instructions=(
            "You are a technology researcher. Analyze the given topic from a "
            "technology and innovation perspective. Keep your analysis to 2-3 paragraphs."
        ),
    )

    business_analyst = client.as_agent(
        name="BusinessAnalyst",
        instructions=(
            "You are a business analyst. Analyze the given topic from a "
            "market and business impact perspective. Keep your analysis to 2-3 paragraphs."
        ),
    )

    social_researcher = client.as_agent(
        name="SocialResearcher",
        instructions=(
            "You are a social impact researcher. Analyze the given topic from a "
            "societal and ethical perspective. Keep your analysis to 2-3 paragraphs."
        ),
    )

    # Build concurrent workflow — all agents process the same input in parallel
    workflow = ConcurrentBuilder(
        participants=[tech_researcher, business_analyst, social_researcher],
    ).build()

    # Execute — all agents run simultaneously
    print("=== Concurrent Multi-Perspective Analysis ===\n")
    query = "The rise of autonomous AI agents in enterprise software"

    print(f"Topic: {query}\n")
    result = await workflow.run(query)

    # Collect results from all parallel agents
    outputs = result.get_outputs()
    labels = ["Technology Perspective", "Business Perspective", "Social Perspective"]

    for label, output in zip(labels, outputs):
        print(f"\n--- {label} ---")
        print(output)
        print()


if __name__ == "__main__":
    asyncio.run(main())
