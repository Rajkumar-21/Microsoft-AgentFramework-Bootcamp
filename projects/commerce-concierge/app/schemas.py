"""Structured output schemas for the concierge."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ShopperIntent(BaseModel):
    """Parsed understanding of what the shopper wants."""

    category: str = Field(description="Product category, e.g. 'jacket'.")
    attributes: list[str] = Field(
        default_factory=list, description="Desired features, e.g. waterproof."
    )
    max_price: float | None = Field(default=None, description="Budget ceiling.")


class ProductPick(BaseModel):
    """A recommended product."""

    sku: str
    name: str
    price: float
    why: str = Field(description="One-sentence reason this fits the shopper.")


class OrderDraft(BaseModel):
    """A prepared (not yet placed) order."""

    sku: str
    quantity: int = 1
    unit_price: float
    shipping_estimate: float
    total: float
    needs_human: bool = Field(
        default=False, description="True if a human must confirm before placing."
    )
