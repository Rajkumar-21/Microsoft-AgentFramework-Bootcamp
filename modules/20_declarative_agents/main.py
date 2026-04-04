"""
Module 20: Declarative Agents
Load agent definitions from YAML config files.
"""

import asyncio
import os
from pathlib import Path

import yaml

from agent_framework.openai import OpenAIChatClient


def load_agent_configs(config_path: str) -> list[dict]:
    """Load agent definitions from YAML file."""
    with open(config_path) as f:
        config = yaml.safe_load(f)
    return config.get("agents", [])


async def main():
    chat_client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )

    # Load agent configs from YAML
    config_path = Path(__file__).parent / "agents.yaml"
    agent_configs = load_agent_configs(str(config_path))

    print(f"Loaded {len(agent_configs)} agent definitions from config\n")

    # Create agents dynamically from config
    agents = {}
    for config in agent_configs:
        agent = chat_client.as_agent(
            name=config["name"],
            instructions=config["instructions"],
        )
        agents[config["name"]] = agent
        print(f"  ✓ Created agent: {config['name']}")

    # Test each agent
    test_queries = {
        "SummaryAgent": (
            "The Microsoft Agent Framework is a comprehensive SDK for building "
            "AI agents. It supports multiple providers including Azure OpenAI "
            "and Azure AI Foundry. Features include function tools, hosted tools, "
            "MCP integration, middleware, workflows, and multi-agent patterns."
        ),
        "TranslatorAgent": "Translate 'Hello, how are you today?' to Spanish and French.",
        "CodeReviewAgent": "Review this Python code:\ndef calc(x,y): return x/y",
    }

    for agent_name, query in test_queries.items():
        print(f"\n{'='*50}")
        print(f"Agent: {agent_name}")
        print(f"Query: {query[:80]}...")
        result = await agents[agent_name].run(query)
        print(f"Response: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
