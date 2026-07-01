"""
Module 12: Workflows — Handoff
Conditional routing based on LLM triage decisions.

HandoffBuilder lets the LLM itself decide which agent to hand off to.
add_handoff(source, targets) declares which agents each source can route to.
The model picks the target at runtime based on agent names/descriptions.
"""

import asyncio
import os

from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import HandoffBuilder


async def main():
    # --- Azure OpenAI client ---
    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )

    # Triage agent — classifies the request and hands off to specialist
    triage = client.as_agent(
        name="Triage",
        description="Customer support triage agent",
        instructions=(
            "You are a customer support triage agent. Classify the customer's request and "
            "hand off to the appropriate specialist:\n"
            "- RefundSpecialist: for returns, refunds, damaged goods\n"
            "- OrderSpecialist: for order status, tracking, delivery issues\n"
            "- GeneralSupport: for account questions, product info, everything else\n"
            "Briefly acknowledge the customer, then hand off."
        ),
    )

    # Specialist agents
    refund_agent = client.as_agent(
        name="RefundSpecialist",
        description="Handles returns and refund requests",
        instructions=(
            "You are a refund specialist. Help customers with returns and refunds. "
            "Be empathetic and provide clear steps for the refund process. "
            "When done, hand off to ResponseFormatter."
        ),
    )

    order_agent = client.as_agent(
        name="OrderSpecialist",
        description="Handles order tracking and delivery issues",
        instructions=(
            "You are an order tracking specialist. Help customers check order status, "
            "track shipments, and resolve delivery issues. "
            "When done, hand off to ResponseFormatter."
        ),
    )

    support_agent = client.as_agent(
        name="GeneralSupport",
        description="Handles general inquiries and account questions",
        instructions=(
            "You are a general support agent. Help with account questions, "
            "product information, and other general inquiries. "
            "When done, hand off to ResponseFormatter."
        ),
    )

    # Final response formatter
    final_agent = client.as_agent(
        name="ResponseFormatter",
        description="Formats final customer-facing response",
        instructions=(
            "You are the final response formatter. Take the specialist's response "
            "and format it into a polished customer-facing message. "
            "Add a case reference number and satisfaction survey link."
        ),
    )

    # Build handoff workflow — LLM decides routing at each step
    builder = HandoffBuilder(
        name="CustomerSupport",
        participants=[triage, refund_agent, order_agent, support_agent, final_agent],
    )
    builder.with_start_agent(triage)
    builder.add_handoff(triage, [refund_agent, order_agent, support_agent])
    builder.add_handoff(refund_agent, [final_agent])
    builder.add_handoff(order_agent, [final_agent])
    builder.add_handoff(support_agent, [final_agent])
    workflow = builder.build()

    # Test with different customer queries
    queries = [
        "I want to return my headphones, they stopped working after 2 days.",
        "Where is my order #12345? It was supposed to arrive yesterday.",
        "How do I change my account email address?",
    ]

    for query in queries:
        print(f"\n{'=' * 60}")
        print(f"Customer: {query}")
        print(f"{'=' * 60}")
        result = await workflow.run(query)
        for output in result.get_outputs():
            print(f"\nFinal Response:\n{output}")


if __name__ == "__main__":
    asyncio.run(main())
