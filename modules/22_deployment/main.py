"""
Module 22: Deployment
Production deployment patterns for Microsoft Agent Framework.
"""

import asyncio
import os

from agent_framework.foundry import FoundryChatClient
from agent_framework.openai import OpenAIChatClient
from azure.identity.aio import DefaultAzureCredential


async def create_production_agent():
    """Create an agent with production-ready configuration."""

    # Production: Use DefaultAzureCredential (supports managed identity)
    credential = DefaultAzureCredential()

    # Option 1: Azure AI Foundry (recommended for production)
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ.get("FOUNDRY_MODEL", "gpt-4o"),
        credential=credential,
    )

    agent = client.as_agent(
        name="ProductionAgent",
        instructions=(
            "You are a production assistant. Provide accurate, "
            "concise responses. Follow safety guidelines strictly."
        ),
    )

    # Health check
    result = await agent.run("Respond with 'OK' if you are operational.")
    print(f"Health check: {result.text}")

    await credential.close()
    return agent


async def main():
    print("=== Production Deployment Patterns ===\n")

    print("1. Authentication: DefaultAzureCredential (auto-selects best method)")
    print("   - Local dev: AzureCliCredential")
    print("   - Production: Managed Identity")
    print("   - CI/CD: Environment variables\n")

    print("2. Environment Variables (set in Azure App Settings):")
    env_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_MODEL",
        "FOUNDRY_PROJECT_ENDPOINT",
        "FOUNDRY_MODEL",
    ]
    for var in env_vars:
        value = os.environ.get(var, "NOT SET")
        print(f"   {var}: {'✓ Set' if value != 'NOT SET' else '✗ Not set'}")

    print("\n3. Deployment Commands:")
    print("   # Build container")
    print("   docker build -t agent-app:latest .")
    print("   # Deploy to Azure Container Apps")
    print("   az containerapp up --name my-agent --image agent-app:latest")
    print("   # Or deploy to Azure Functions")
    print("   func azure functionapp publish my-agent-func")

    print("\n4. Running production agent...")
    try:
        await create_production_agent()
    except Exception as e:
        print(f"   Note: {e}")
        print("   (Set up Azure credentials to run this in production)")


if __name__ == "__main__":
    asyncio.run(main())
