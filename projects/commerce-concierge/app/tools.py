"""Function tools for catalog, reviews, inventory, and shipping."""

from __future__ import annotations

from typing import Annotated

from agent_framework import tool
from pydantic import Field

_CATALOG = [
    {"sku": "JKT-100", "name": "TrailShield Waterproof Jacket", "price": 139.0},
    {"sku": "JKT-200", "name": "Summit Insulated Parka", "price": 189.0},
    {"sku": "JKT-300", "name": "RainLite Packable Shell", "price": 89.0},
]


@tool
def search_catalog(
    query: Annotated[str, Field(description="Search keywords.")],
) -> str:
    """Search the product catalog (simulated)."""
    hits = [p for p in _CATALOG if any(w in p["name"].lower() for w in query.lower().split())]
    hits = hits or _CATALOG
    return "; ".join(f"{p['sku']} {p['name']} ${p['price']}" for p in hits)


@tool
def get_reviews(sku: Annotated[str, Field(description="Product SKU.")]) -> str:
    """Return a review summary for a SKU (simulated)."""
    return f"{sku}: 4.5/5 from 320 reviews — praised for waterproofing, runs slightly large."


@tool
def check_inventory(sku: Annotated[str, Field(description="Product SKU.")]) -> str:
    """Check stock for a SKU (simulated)."""
    return f"{sku}: 42 units in stock, ships in 1-2 business days."


@tool
def estimate_shipping(
    sku: Annotated[str, Field(description="Product SKU.")],
    zip_code: Annotated[str, Field(description="Destination ZIP/postal code.")] = "00000",
) -> str:
    """Estimate shipping cost to a destination (simulated)."""
    return f"Standard shipping for {sku} to {zip_code}: $7.99 (3-5 days)."
