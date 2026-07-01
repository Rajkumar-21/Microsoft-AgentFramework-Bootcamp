"""Compose the concierge pipeline from sub-workflows.

Stages:
  1. Understand     (single agent, structured intent)
  2. Research       (concurrent: catalog ∥ reviews ∥ inventory)
  3. Recommend      (single agent, structured pick)
  4. Quote          (single agent, structured order draft)

The handoff to human support is wired separately so the concierge can escalate
when ``OrderDraft.needs_human`` is true.
"""

from __future__ import annotations

from agent_framework import ConcurrentBuilder, HandoffBuilder, SequentialBuilder

from .agents import build_agents


async def build_concierge_workflow():
    agents = await build_agents()

    research = ConcurrentBuilder(
        participants=[agents["catalog"], agents["reviews"], agents["inventory"]]
    ).build()

    # The research sub-workflow runs as one participant inside the main pipeline.
    pipeline = SequentialBuilder(
        participants=[
            agents["understand"],
            research.as_agent(name="Research"),
            agents["recommend"],
            agents["quote"],
        ]
    ).build()

    # Wrap the pipeline with a handoff to human support for escalations.
    concierge = (
        HandoffBuilder(
            participants=[pipeline.as_agent(name="Pipeline"), agents["support"]]
        )
        .build()
    )
    return concierge
