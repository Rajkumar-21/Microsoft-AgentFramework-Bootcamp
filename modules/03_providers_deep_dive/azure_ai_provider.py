"""
Module 03 — Providers Deep Dive (B): Azure AI Foundry
=====================================================

Scenario: Northwind IT — Service Desk Triage (Foundry edition)
--------------------------------------------------------------
This is the *same* triage agent as `azure_openai_provider.py`, but backed by a
model deployed in an **Azure AI Foundry** project. Notice that `TRIAGE_INSTRUCTIONS`
and the `create_agent(...)` / `run(...)` calls are identical — only the client
differs. That portability is a core Agent Framework design goal.

`AzureAIAgentClient` uses keyless auth via `DefaultAzureCredential` and reads
`AZURE_AI_PROJECT_ENDPOINT` + `AZURE_AI_MODEL_DEPLOYMENT_NAME` from the
environment. Run `az login` first for local development.
"""

import asyncio

from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential


TRIAGE_INSTRUCTIONS = """\
You are the Northwind IT Service Desk triage agent.
For each ticket, respond with exactly three lines:
  Priority: <P1|P2|P3|P4>   (P1 = outage/security, P4 = how-to question)
  Queue: <Network|Identity|Hardware|Software|Security>
  Summary: <one sentence>
Be decisive. Do not ask follow-up questions."""

SAMPLE_TICKET = (
    "A finance manager reports a phishing email that asks for MFA codes; "
    "three people may have clicked the link. Needs urgent attention."
)


async def main() -> None:
    # The credential is async — use it as an async context manager so tokens
    # are acquired and disposed cleanly.
    async with AzureCliCredential() as credential:
        client = AzureAIAgentClient(async_credential=credential)

        agent = client.create_agent(name="ITTriageAgent", instructions=TRIAGE_INSTRUCTIONS)

        print(f"Ticket: {SAMPLE_TICKET}\n")
        response = await agent.run(SAMPLE_TICKET)
        print("[Azure AI Foundry]")
        print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
