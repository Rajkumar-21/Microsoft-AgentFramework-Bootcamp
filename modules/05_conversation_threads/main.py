"""
Module 05 — Conversation Threads
================================

Scenario: Summit Bank — Mortgage Pre-Qualification Interview
------------------------------------------------------------
A pre-qualification advisor that interviews an applicant across several turns.
The agent must *remember* what was said earlier — income, down payment, target
price — and use it when the applicant asks for a summary or a decision.

The mechanism is the **thread**:
  * `thread = agent.get_new_thread()` creates a fresh conversation (sync call).
  * Passing `thread=thread` into every `agent.run(...)` carries history forward.
  * Omit the thread and each call is stateless — the agent forgets everything.

This module runs the same questions twice: once *with* a shared thread (the
agent remembers) and once *without* (it forgets) to make the difference obvious.
"""

import asyncio
import os

from agent_framework.azure import AzureOpenAIChatClient


ADVISOR_INSTRUCTIONS = """\
You are a mortgage pre-qualification advisor at Summit Bank.
Collect the applicant's annual income, available down payment, and target home
price over the conversation. When asked, summarize what you know and give a
rough pre-qualification view using a 28% front-end ratio as a guideline.
Keep replies short. Never ask for SSN or account numbers."""

TURNS = [
    "Hi — my household income is $140,000 a year.",
    "We've saved $60,000 for a down payment.",
    "We're looking at homes around $480,000.",
    "Based on everything I told you, do we pre-qualify? Summarize first.",
]


def build_client() -> AzureOpenAIChatClient:
    deployment = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME") or os.environ["AZURE_OPENAI_MODEL"]
    return AzureOpenAIChatClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        deployment_name=deployment,
    )


async def run_with_memory(agent) -> None:
    print("=" * 64)
    print("  WITH a shared thread — the agent remembers")
    print("=" * 64)
    thread = agent.get_new_thread()  # sync; carries history across run() calls
    for message in TURNS:
        print(f"\nApplicant: {message}")
        response = await agent.run(message, thread=thread)
        print(f"Advisor:   {response.text}")


async def run_without_memory(agent) -> None:
    print("\n" + "=" * 64)
    print("  WITHOUT a thread — each turn is stateless")
    print("=" * 64)
    for message in TURNS:
        print(f"\nApplicant: {message}")
        response = await agent.run(message)  # no thread -> no memory
        print(f"Advisor:   {response.text}")


async def main() -> None:
    client = build_client()
    agent = client.create_agent(name="MortgageAdvisor", instructions=ADVISOR_INSTRUCTIONS)

    await run_with_memory(agent)
    await run_without_memory(agent)


if __name__ == "__main__":
    asyncio.run(main())
