"""Sample catalog data, loaded on startup in dev mode."""

from __future__ import annotations

from .models import (
    Agent,
    AgentProtocol,
    AgentSkillRef,
    AuthType,
    MCPServer,
    MCPToolRef,
    MCPTransport,
    Publisher,
    Skill,
    SkillKind,
)
from .storage.base import RegistryStore

_BOOTCAMP = Publisher(id="bootcamp", name="Agent Framework Bootcamp")


def _sample_agents() -> list[Agent]:
    return [
        Agent(
            name="Atlas Support Agent",
            summary="Customer support agent deployed on Azure Functions.",
            description=(
                "Handles tier-1 support tickets with knowledge-base lookups and "
                "escalation. Built in lesson 22 (Deployment)."
            ),
            endpoint="https://atlas-support-prod.azurewebsites.net/api/agents/Atlas/run",
            protocol=AgentProtocol.azure_functions,
            auth=AuthType.entra,
            scopes=["Atlas.Invoke"],
            tags=["support", "azure-functions", "production"],
            publisher=_BOOTCAMP,
            partition_key=_BOOTCAMP.id,
            skills=[
                AgentSkillRef(id="kb", name="Knowledge base", description="Search docs"),
                AgentSkillRef(id="esc", name="Escalate", description="Route to human"),
            ],
        ),
        Agent(
            name="Nexus Concierge",
            summary="A2A concierge that federates partner agents as tools.",
            description=(
                "Discovers partner agents via their agent cards and calls them as "
                "tools. Built in lesson 21 (Agent-to-Agent)."
            ),
            endpoint="https://nexus.contoso.com/a2a",
            protocol=AgentProtocol.a2a,
            auth=AuthType.entra,
            scopes=["Nexus.Federate"],
            tags=["a2a", "concierge", "federation"],
            publisher=_BOOTCAMP,
            partition_key=_BOOTCAMP.id,
        ),
        Agent(
            name="Meridian Operations Center",
            summary="Magentic supervisor orchestrating an ops incident workflow.",
            description=(
                "Capstone agent combining MCP tools, middleware, HITL approvals, "
                "memory, and observability behind a Magentic manager."
            ),
            endpoint="https://meridian-ops.azurewebsites.net/api/agents/Meridian/run",
            protocol=AgentProtocol.azure_functions,
            auth=AuthType.entra,
            scopes=["Meridian.Operate"],
            tags=["supervisor", "magentic", "operations", "capstone"],
            publisher=_BOOTCAMP,
            partition_key=_BOOTCAMP.id,
        ),
    ]


def _sample_mcp_servers() -> list[MCPServer]:
    return [
        MCPServer(
            name="Azure Docs MCP",
            summary="Streamable-HTTP MCP server exposing Microsoft Learn search.",
            description="Wraps Microsoft Learn docs search and fetch as MCP tools.",
            url="https://learn.microsoft.com/api/mcp",
            transport=MCPTransport.streamable_http,
            auth=AuthType.none,
            tags=["docs", "microsoft-learn", "search"],
            publisher=_BOOTCAMP,
            partition_key=_BOOTCAMP.id,
            tools=[
                MCPToolRef(name="microsoft_docs_search", description="Search docs"),
                MCPToolRef(name="microsoft_docs_fetch", description="Fetch a doc page"),
            ],
        ),
        MCPServer(
            name="Ops Toolkit MCP",
            summary="Incident tooling: paging, runbooks, and ticket creation.",
            description="Internal MCP server used by the Meridian capstone agent.",
            url="https://ops-toolkit.contoso.com/mcp",
            transport=MCPTransport.streamable_http,
            auth=AuthType.entra,
            scopes=["Ops.Tools"],
            tags=["operations", "incident", "internal"],
            publisher=_BOOTCAMP,
            partition_key=_BOOTCAMP.id,
            tools=[
                MCPToolRef(name="page_oncall", description="Page the on-call engineer"),
                MCPToolRef(name="create_ticket", description="Open an incident ticket"),
            ],
        ),
    ]


def _sample_skills() -> list[Skill]:
    triage_yaml = (
        "kind: prompt\n"
        "name: incident_triage\n"
        "instructions: |\n"
        "  You are an SRE triage assistant. Given an alert, classify severity\n"
        "  (sev1-sev4), summarize impact, and propose the first mitigation step.\n"
        "inputs: [alert]\n"
        "outputs: [severity, summary, next_step]\n"
    )
    return [
        Skill(
            name="Incident Triage",
            summary="Prompt skill that classifies and summarizes incident alerts.",
            description="Reusable declarative prompt agent for SRE triage.",
            skill_kind=SkillKind.prompt,
            spec=triage_yaml,
            inputs=["alert"],
            outputs=["severity", "summary", "next_step"],
            tags=["sre", "triage", "prompt"],
            publisher=_BOOTCAMP,
            partition_key=_BOOTCAMP.id,
        ),
        Skill(
            name="Sentiment Tag",
            summary="Tool skill that scores message sentiment for routing.",
            description="Function-tool contract returning a -1..1 sentiment score.",
            skill_kind=SkillKind.tool,
            spec="def score_sentiment(text: str) -> float: ...",
            inputs=["text"],
            outputs=["score"],
            tags=["nlp", "routing", "tool"],
            publisher=_BOOTCAMP,
            partition_key=_BOOTCAMP.id,
        ),
    ]


async def seed_catalog(store: RegistryStore) -> None:
    """Insert sample resources. Safe to call once on startup."""
    for agent in _sample_agents():
        await store.create(agent)
    for server in _sample_mcp_servers():
        await store.create(server)
    for skill in _sample_skills():
        await store.create(skill)
