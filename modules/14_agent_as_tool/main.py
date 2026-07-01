"""
Module 14: Agent-as-Tool
Use agents as tools for other agents (hierarchical delegation).

agent.as_tool() wraps an agent as a FunctionTool so a parent agent
can delegate subtasks to specialist child agents.
"""

import asyncio
import os

from agent_framework.openai import OpenAIChatClient


async def main():
    # --- Azure OpenAI client ---
    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )

    # Create specialist agents
    code_expert = client.as_agent(
        name="CodeExpert",
        instructions=(
            "You are a Python coding expert. When asked about coding topics, "
            "provide clear explanations with code examples. Keep responses focused."
        ),
    )

    devops_expert = client.as_agent(
        name="DevOpsExpert",
        instructions=(
            "You are a DevOps expert specializing in CI/CD, Docker, Kubernetes, "
            "and cloud infrastructure. Provide practical, actionable advice."
        ),
    )

    architecture_expert = client.as_agent(
        name="ArchitectureExpert",
        instructions=(
            "You are a software architecture expert. Provide guidance on "
            "system design, patterns, scalability, and best practices."
        ),
    )

    # Create the main orchestrator that uses specialists as tools
    lead_engineer = client.as_agent(
        name="LeadEngineer",
        instructions=(
            "You are a Lead Software Engineer. For technical questions, "
            "delegate to your team of specialists:\n"
            "- CodeExpert: For Python coding questions\n"
            "- DevOpsExpert: For infrastructure and deployment questions\n"
            "- ArchitectureExpert: For system design questions\n\n"
            "Analyze the question, delegate to the right specialist, "
            "and synthesize their response with your own insights."
        ),
        tools=[
            code_expert.as_tool(),
            devops_expert.as_tool(),
            architecture_expert.as_tool(),
        ],
    )

    # Test with different types of questions
    queries = [
        "How should I implement async database access in Python?",
        "What's the best way to set up a CI/CD pipeline for microservices?",
        "How should I design a system that handles 10M requests per day?",
    ]

    for query in queries:
        print(f"\n{'=' * 60}")
        print(f"Question: {query}")
        print(f"{'=' * 60}")
        result = await lead_engineer.run(query)
        print(f"\nLead Engineer: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
