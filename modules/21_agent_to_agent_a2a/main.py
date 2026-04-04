"""
Module 21: Agent-to-Agent Communication (A2A)
Agents communicating via standardized protocols.

NOTE: A2A is an emerging protocol. This module demonstrates the concepts.
Check the latest agent-framework docs for current A2A API support.
"""

import asyncio
import os
from typing import Annotated

from pydantic import BaseModel, Field

from agent_framework import tool
from agent_framework.openai import OpenAIChatClient


# Simulated A2A Agent Card
class AgentCard(BaseModel):
    """Agent capability description for A2A discovery."""

    name: str
    description: str
    capabilities: list[str]
    input_format: str
    output_format: str


# Define agent cards (capability descriptions)
AGENT_REGISTRY = {
    "DataAnalyst": AgentCard(
        name="DataAnalyst",
        description="Analyzes data and provides statistical insights",
        capabilities=["data_analysis", "statistics", "visualization_recommendations"],
        input_format="text description of data or analysis request",
        output_format="analysis report with findings and recommendations",
    ),
    "ReportWriter": AgentCard(
        name="ReportWriter",
        description="Generates formatted reports from analysis",
        capabilities=["report_generation", "formatting", "executive_summaries"],
        input_format="analysis findings and data",
        output_format="formatted report document",
    ),
}


@tool
def discover_agent(
    capability: Annotated[str, Field(description="Required capability to search for")],
) -> str:
    """Discover agents by capability (A2A-style agent discovery)."""
    matches = []
    for name, card in AGENT_REGISTRY.items():
        if capability.lower() in [c.lower() for c in card.capabilities]:
            matches.append(f"{card.name}: {card.description}")
    return f"Found agents: {', '.join(matches)}" if matches else "No agents found"


async def main():
    chat_client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )

    # Agent 1: Data Analyst
    analyst = chat_client.as_agent(
        name="DataAnalyst",
        instructions=(
            "You are a data analyst. Analyze data requests and provide "
            "statistical insights and findings in a structured format."
        ),
    )

    # Agent 2: Report Writer
    writer = chat_client.as_agent(
        name="ReportWriter",
        instructions=(
            "You are a report writer. Take analysis findings and create "
            "a polished executive report with recommendations."
        ),
    )

    # Orchestrator with agent discovery
    orchestrator = chat_client.as_agent(
        name="Orchestrator",
        instructions=(
            "You are an orchestrator. Use agent discovery to find "
            "the right agent for each task. Coordinate between agents "
            "to fulfill complex requests."
        ),
        tools=[discover_agent, analyst.as_tool(), writer.as_tool()],
    )

    # A2A-style communication
    print("=== A2A Agent Communication ===\n")

    # Step 1: Discover agents
    print("Agent Registry:")
    for name, card in AGENT_REGISTRY.items():
        print(f"  📋 {card.name}: {card.description}")
        print(f"     Capabilities: {', '.join(card.capabilities)}")
    print()

    # Step 2: Orchestrate multi-agent task
    result = await orchestrator.run(
        "Analyze the trend of AI agent adoption in enterprise software "
        "over the past 3 years, then create an executive report with recommendations."
    )
    print(f"Final Report:\n{result.text}")


if __name__ == "__main__":
    asyncio.run(main())
