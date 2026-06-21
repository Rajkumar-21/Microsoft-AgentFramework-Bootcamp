"""
Module 03 — Providers Deep Dive (A): Azure OpenAI
=================================================

Scenario: Northwind IT — Service Desk Triage
--------------------------------------------
The IT help desk wants every inbound ticket auto-classified by priority and
routed to the right queue. This file implements that triage agent on
**Azure OpenAI**. Its twin, `azure_ai_provider.py`, implements the *exact same*
agent on **Azure AI Foundry** — proving how portable an Agent Framework agent is
across providers. Only the client construction changes; the agent code is identical.

Auth options shown:
  * API key (simplest for local dev)
  * `AzureCliCredential` (keyless — recommended, run `az login` first)
"""

import asyncio
import os

from agent_framework.azure import AzureOpenAIChatClient
from azure.identity.aio import AzureCliCredential


TRIAGE_INSTRUCTIONS = """\
You are the Northwind IT Service Desk triage agent.
For each ticket, respond with exactly three lines:
  Priority: <P1|P2|P3|P4>   (P1 = outage/security, P4 = how-to question)
  Queue: <Network|Identity|Hardware|Software|Security>
  Summary: <one sentence>
Be decisive. Do not ask follow-up questions."""

SAMPLE_TICKET = (
    "Half the 3rd-floor office can't reach any internal site since 9am. "
    "VPN users are fine. Started right after the morning switch maintenance."
)


def build_client() -> AzureOpenAIChatClient:
    """Construct an Azure OpenAI client.

    Prefers keyless auth via Azure CLI credentials; falls back to an API key
    when one is present in the environment.
    """
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    deployment = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME") or os.environ["AZURE_OPENAI_MODEL"]

    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    if api_key:
        return AzureOpenAIChatClient(endpoint=endpoint, deployment_name=deployment, api_key=api_key)
    return AzureOpenAIChatClient(
        endpoint=endpoint, deployment_name=deployment, credential=AzureCliCredential()
    )


async def main() -> None:
    client = build_client()

    agent = client.create_agent(name="ITTriageAgent", instructions=TRIAGE_INSTRUCTIONS)

    print(f"Ticket: {SAMPLE_TICKET}\n")
    response = await agent.run(SAMPLE_TICKET)
    print("[Azure OpenAI]")
    print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
