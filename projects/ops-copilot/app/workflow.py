"""Magentic supervisor that orchestrates triage → mitigation → comms."""

from __future__ import annotations

from agent_framework import MagenticBuilder
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential

from .agents import build_agents


async def build_incident_workflow():
    """Build a Magentic workflow with the three specialist agents."""
    agents = await build_agents()
    manager_client = AzureOpenAIChatClient(credential=DefaultAzureCredential())

    workflow = (
        MagenticBuilder()
        .participants(
            triage=agents["triage"],
            mitigation=agents["mitigation"],
            comms=agents["comms"],
        )
        .with_standard_manager(
            chat_client=manager_client,
            max_round_count=12,
            max_stall_count=3,
            max_reset_count=1,
        )
        .build()
    )
    return workflow
