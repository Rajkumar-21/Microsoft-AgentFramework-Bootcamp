"""
Module 15: Multi-Agent Supervisor
Central coordinator that delegates to specialist agents.

Combines function @tools and agent.as_tool() in a single supervisor agent.
"""

import asyncio
import os
from typing import Annotated

from pydantic import Field

from agent_framework import tool
from agent_framework.openai import OpenAIChatClient


# ---------------------------------------------------------------------------
# Custom function tools for the supervisor
# ---------------------------------------------------------------------------
@tool
def get_team_availability(
    team: Annotated[str, Field(description="Team name: frontend, backend, devops, qa")],
) -> str:
    """Check team availability for task assignment."""
    availability = {
        "frontend": "3 developers available, 1 on leave",
        "backend": "4 developers available, 2 busy with sprint",
        "devops": "2 engineers available",
        "qa": "2 testers available, 1 on automation tasks",
    }
    return availability.get(team.lower(), f"Unknown team: {team}")


@tool
def estimate_timeline(
    complexity: Annotated[str, Field(description="Task complexity: low, medium, high")],
    team_size: Annotated[int, Field(description="Number of team members")],
) -> str:
    """Estimate project timeline based on complexity and team size."""
    base_days = {"low": 5, "medium": 15, "high": 30}
    days = base_days.get(complexity.lower(), 15) / max(team_size, 1)
    return f"Estimated: {days:.0f} business days with {team_size} team members"


async def main():
    # --- Azure OpenAI client ---
    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )

    # Specialist agents
    frontend_lead = client.as_agent(
        name="FrontendLead",
        instructions=(
            "You are a frontend tech lead. When asked about UI features, "
            "provide technical breakdown, component design, and effort estimates."
        ),
    )

    backend_lead = client.as_agent(
        name="BackendLead",
        instructions=(
            "You are a backend tech lead. When asked about API/service features, "
            "provide architecture, endpoints, data models, and effort estimates."
        ),
    )

    qa_lead = client.as_agent(
        name="QALead",
        instructions=(
            "You are a QA lead. When asked about testing, provide test strategy, "
            "test cases, automation plan, and effort estimates."
        ),
    )

    # Supervisor agent with both agent-as-tool and function tools
    project_manager = client.as_agent(
        name="ProjectManager",
        instructions=(
            "You are a Senior Project Manager. Your job is to:\n"
            "1. Analyze feature requests and break them into technical tasks\n"
            "2. Check team availability using the tool\n"
            "3. Delegate technical analysis to the right lead (Frontend, Backend, QA)\n"
            "4. Estimate timelines\n"
            "5. Create a consolidated project plan\n\n"
            "Always check availability first, then delegate to specialists, "
            "then provide a final consolidated plan."
        ),
        tools=[
            get_team_availability,
            estimate_timeline,
            frontend_lead.as_tool(),
            backend_lead.as_tool(),
            qa_lead.as_tool(),
        ],
    )

    # Run the supervisor
    print("=== Project Manager Supervisor ===\n")
    result = await project_manager.run(
        "We need to build a real-time notification system for our web app. "
        "Users should receive push notifications, email alerts, and in-app messages. "
        "Create a project plan with team assignments and timeline."
    )
    print(f"Project Plan:\n{result.text}")


if __name__ == "__main__":
    asyncio.run(main())
