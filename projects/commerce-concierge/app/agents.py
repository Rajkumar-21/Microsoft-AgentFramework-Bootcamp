"""Build the concierge's specialist agents."""

from __future__ import annotations

from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential

from .registry import discover_warehouse_url
from .schemas import OrderDraft, ProductPick, ShopperIntent
from .tools import check_inventory, estimate_shipping, get_reviews, search_catalog


def _client() -> AzureOpenAIChatClient:
    return AzureOpenAIChatClient(credential=DefaultAzureCredential())


async def build_agents() -> dict[str, object]:
    client = _client()

    understand = client.create_agent(
        name="Understand",
        instructions=(
            "Extract the shopper's intent: category, desired attributes, and "
            "budget. Respond as structured data only."
        ),
        response_format=ShopperIntent,
    )

    # Concurrent research specialists.
    catalog = client.create_agent(
        name="Catalog",
        instructions="Find matching products using the catalog tool.",
        tools=[search_catalog],
    )
    reviews = client.create_agent(
        name="Reviews",
        instructions="Summarize reviews for candidate products.",
        tools=[get_reviews],
    )
    inventory = client.create_agent(
        name="Inventory",
        instructions="Check stock and lead time for candidate products.",
        tools=[check_inventory],
    )

    recommend = client.create_agent(
        name="Recommend",
        instructions=(
            "Pick the single best product for the shopper given the research. "
            "Respond as a structured ProductPick."
        ),
        response_format=ProductPick,
    )

    quote = client.create_agent(
        name="Quote",
        instructions=(
            "Prepare an OrderDraft for the chosen product, including a shipping "
            "estimate. Set needs_human=true if the price is over $150 or the "
            "request is ambiguous."
        ),
        tools=[estimate_shipping],
        response_format=OrderDraft,
    )

    support = client.create_agent(
        name="HumanSupport",
        instructions=(
            "You are a human-support liaison. When the concierge escalates, "
            "summarize the situation and the next step a human should take."
        ),
    )

    # Warehouse agent reached over A2A (discovered from the registry).
    warehouse = await _build_warehouse_agent()

    return {
        "understand": understand,
        "catalog": catalog,
        "reviews": reviews,
        "inventory": inventory,
        "recommend": recommend,
        "quote": quote,
        "support": support,
        "warehouse": warehouse,
    }


async def _build_warehouse_agent():
    """Connect to the warehouse agent over A2A, if available."""
    url = await discover_warehouse_url()
    if not url:
        return None
    try:
        from agent_framework.a2a import A2AAgent

        return A2AAgent(name="Warehouse", url=url)
    except Exception:
        return None
