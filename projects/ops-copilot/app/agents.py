"""Build the triage, mitigation, and comms agents."""

from __future__ import annotations

from agent_framework import ChatMessageStore
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential

from .middleware import audit_middleware
from .registry import discover_mcp_tools
from .tools import get_metric, lookup_runbook, restart_service


def _chat_client() -> AzureOpenAIChatClient:
    # Uses AZURE_OPENAI_* env vars. Managed identity when no API key is set.
    return AzureOpenAIChatClient(credential=DefaultAzureCredential())


async def build_agents() -> dict[str, object]:
    """Create the three specialist agents. Mitigation gets registry MCP tools."""
    client = _chat_client()
    mcp_tools = await discover_mcp_tools(tag="operations")

    triage = client.create_agent(
        name="Triage",
        instructions=(
            "You are an SRE triage specialist. Given an alert, determine "
            "severity (sev1-sev4), summarize the impact, and read the relevant "
            "metric and runbook. Be concise and factual."
        ),
        tools=[get_metric, lookup_runbook],
        middleware=[audit_middleware],
    )

    mitigation = client.create_agent(
        name="Mitigation",
        instructions=(
            "You propose and, after human approval, execute mitigation steps. "
            "Prefer the least disruptive action. Use registry MCP tools for "
            "paging or ticketing when needed. Never act without approval."
        ),
        tools=[restart_service, *mcp_tools],
        middleware=[audit_middleware],
        # Remember the incident timeline across turns.
        chat_message_store_factory=ChatMessageStore,
    )

    comms = client.create_agent(
        name="Comms",
        instructions=(
            "You draft clear, non-technical status updates for stakeholders "
            "based on the triage and mitigation so far. Keep it under 80 words."
        ),
        middleware=[audit_middleware],
    )

    return {"triage": triage, "mitigation": mitigation, "comms": comms}
