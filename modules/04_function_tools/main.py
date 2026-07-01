"""
Module 04 — Function Tools
==========================

Scenario: Lakeside Outfitters — Order Operations Agent
------------------------------------------------------
A support agent for an e-commerce ops team. It can look up an order, check
warehouse stock, estimate a delivery date, and start a refund — all by calling
typed Python functions the model invokes on demand.

Key ideas:
  * Tools are plain Python functions. Type hints + `Annotated[..., Field(...)]`
    descriptions tell the model how to call them; the docstring becomes the
    tool description.
  * Pass them with `create_agent(..., tools=[fn1, fn2, ...])`.
  * The model decides *which* tool(s) to call and *when* — including chaining
    several in one turn.

This module uses in-memory fixtures so it runs without external systems.
"""

import asyncio
import os
from datetime import date, timedelta
from typing import Annotated

from agent_framework.azure import AzureOpenAIChatClient
from pydantic import Field


# --- Fake systems of record (stand-ins for OMS / WMS / payments) -------------
_ORDERS = {
    "LO-10231": {"status": "packed", "sku": "TENT-4P", "qty": 1, "region": "WA"},
    "LO-10477": {"status": "shipped", "sku": "BAG-65L", "qty": 2, "region": "NY"},
    "LO-10588": {"status": "processing", "sku": "STOVE-X2", "qty": 1, "region": "TX"},
}
_INVENTORY = {"TENT-4P": 14, "BAG-65L": 0, "STOVE-X2": 37}
_TRANSIT_DAYS = {"WA": 2, "NY": 4, "TX": 3}


def lookup_order_status(
    order_id: Annotated[str, Field(description="Order ID, e.g. 'LO-10231'")],
) -> str:
    """Return the current fulfillment status of an order."""
    order = _ORDERS.get(order_id.upper())
    if not order:
        return f"No order found with ID {order_id}."
    return f"Order {order_id.upper()} is '{order['status']}' ({order['qty']}x {order['sku']})."


def check_inventory(
    sku: Annotated[str, Field(description="Product SKU, e.g. 'TENT-4P'")],
) -> str:
    """Check how many units of a SKU are available in the warehouse."""
    if sku.upper() not in _INVENTORY:
        return f"SKU {sku} is not in the catalog."
    count = _INVENTORY[sku.upper()]
    state = "out of stock" if count == 0 else f"{count} units available"
    return f"{sku.upper()}: {state}."


def estimate_delivery(
    order_id: Annotated[str, Field(description="Order ID to estimate delivery for")],
) -> str:
    """Estimate the delivery date for an order based on its destination region."""
    order = _ORDERS.get(order_id.upper())
    if not order:
        return f"No order found with ID {order_id}."
    days = _TRANSIT_DAYS.get(order["region"], 5)
    eta = date.today() + timedelta(days=days)
    return f"Order {order_id.upper()} should arrive around {eta.isoformat()} ({days} days)."


def initiate_refund(
    order_id: Annotated[str, Field(description="Order ID to refund")],
    reason: Annotated[str, Field(description="Short reason for the refund")],
) -> str:
    """Start a refund for an order. Returns a refund reference number."""
    order = _ORDERS.get(order_id.upper())
    if not order:
        return f"Cannot refund — no order found with ID {order_id}."
    ref = f"RF-{order_id.upper()[-5:]}"
    return f"Refund {ref} initiated for {order_id.upper()} (reason: {reason})."


def build_client() -> AzureOpenAIChatClient:
    deployment = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME") or os.environ["AZURE_OPENAI_MODEL"]
    return AzureOpenAIChatClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        deployment_name=deployment,
    )


async def main() -> None:
    client = build_client()

    agent = client.create_agent(
        name="OrderOpsAgent",
        instructions=(
            "You are Lakeside Outfitters' order operations assistant. "
            "Use the available tools to answer questions about orders, stock, "
            "delivery dates, and refunds. Be concise and confirm actions you take."
        ),
        tools=[lookup_order_status, check_inventory, estimate_delivery, initiate_refund],
    )

    conversations = [
        "What's the status of order LO-10231 and when will it arrive?",
        "Is BAG-65L in stock? Order LO-10477 has 2 of them.",
        "Refund order LO-10588 — the customer changed their mind.",
    ]

    for query in conversations:
        print(f"\nUser:  {query}")
        response = await agent.run(query)
        print(f"Agent: {response.text}")


if __name__ == "__main__":
    asyncio.run(main())
