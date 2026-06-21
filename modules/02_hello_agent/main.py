"""
Module 02 — Hello Agent
=======================

Scenario: Contoso Financial — Expense Policy Assistant
------------------------------------------------------
Finance gets the same questions every month ("Can I expense a client dinner?",
"What's the per-diem in Tokyo?"). Your first agent is a front-line assistant
that answers employees from the company's expense policy in plain language.

Demonstrates the canonical Agent Framework 1.8.x flow:
  * Build an `AzureOpenAIChatClient` from environment variables
  * Create an agent with `client.create_agent(...)`
  * Run it with `await agent.run(...)` and read `response.text`

Prerequisites: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY,
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME (see Module 01).
"""

import asyncio
import os

from agent_framework.azure import AzureOpenAIChatClient


SYSTEM_PROMPT = """\
You are the Contoso Financial Expense Policy Assistant.
Answer employee questions about expense reporting clearly and concisely.
Ground every answer in these policy rules:
  - Meals: up to $75/day domestic, $120/day international (receipts required over $25).
  - Client entertainment: pre-approval required from a director; cap $200/person.
  - Airfare: economy for flights under 6 hours; premium economy allowed beyond.
  - Reimbursement window: submit within 30 days of the expense date.
If a question falls outside policy, say so and recommend contacting finance@contoso.com.
Never invent figures that are not in the rules above."""


def build_client() -> AzureOpenAIChatClient:
    """Create the Azure OpenAI chat client from environment variables."""
    deployment = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME") or os.environ["AZURE_OPENAI_MODEL"]
    return AzureOpenAIChatClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        deployment_name=deployment,
    )


async def main() -> None:
    client = build_client()

    agent = client.create_agent(
        name="ExpensePolicyAssistant",
        instructions=SYSTEM_PROMPT,
    )

    question = "I took a client to dinner in Seattle and it cost $90 per person. Can I expense it?"
    print(f"User:  {question}")

    response = await agent.run(question)
    print(f"Agent: {response.text}")


if __name__ == "__main__":
    asyncio.run(main())
