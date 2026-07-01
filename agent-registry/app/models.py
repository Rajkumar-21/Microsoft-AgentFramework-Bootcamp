"""Pydantic models for registry resources: Agents, MCP servers, and Skills.

The data model follows a multi-variant pattern:
  * ``*Create``  — request body when publishing a new resource.
  * ``*Update``  — request body when updating (bumps the version).
  * ``Agent`` / ``MCPServer`` / ``Skill`` — the stored / returned document.

All stored documents share :class:`ResourceBase` (id, version, ownership,
visibility, timestamps) so the storage layer can treat them uniformly.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Annotated, Generic, Literal, TypeVar

from pydantic import BaseModel, Field, HttpUrl


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _new_id() -> str:
    return uuid.uuid4().hex


class ResourceKind(str, Enum):
    agent = "agent"
    mcp_server = "mcp_server"
    skill = "skill"


class Visibility(str, Enum):
    public = "public"          # discoverable by any authenticated consumer
    private = "private"        # discoverable only within the publisher org


# --------------------------------------------------------------------------- #
# Shared metadata
# --------------------------------------------------------------------------- #
class Publisher(BaseModel):
    """Who owns a resource. Derived from the caller's verified token."""

    id: str = Field(..., description="Stable publisher id (tenant or app/user oid).")
    name: str = Field(..., description="Human-friendly publisher name.")


class ResourceBase(BaseModel):
    id: str = Field(default_factory=_new_id)
    kind: ResourceKind
    name: str = Field(..., min_length=2, max_length=80)
    summary: str = Field(..., max_length=280)
    description: str = Field("", max_length=4000)
    version: str = Field("1.0.0", pattern=r"^\d+\.\d+\.\d+$")
    tags: list[str] = Field(default_factory=list)
    visibility: Visibility = Visibility.public
    publisher: Publisher
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)
    # Cosmos partition key — high-cardinality, publisher-scoped queries.
    partition_key: str = Field("", description="Equals publisher.id; set on save.")


# --------------------------------------------------------------------------- #
# Agents
# --------------------------------------------------------------------------- #
class AgentProtocol(str, Enum):
    a2a = "a2a"                      # Agent-to-Agent over HTTP/JSON-RPC
    openai = "openai"                # OpenAI-compatible chat endpoint
    azure_functions = "azure_functions"  # AgentFunctionApp run endpoint


class AuthType(str, Enum):
    none = "none"
    api_key = "api_key"
    entra = "entra"                  # OAuth2 bearer (Microsoft Entra ID)


class AgentSkillRef(BaseModel):
    """A capability advertised by an agent (mirrors an A2A agent card skill)."""

    id: str
    name: str
    description: str = ""


class AgentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    summary: str = Field(..., max_length=280)
    description: str = ""
    endpoint: HttpUrl
    protocol: AgentProtocol = AgentProtocol.a2a
    auth: AuthType = AuthType.entra
    scopes: list[str] = Field(default_factory=list)
    skills: list[AgentSkillRef] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    visibility: Visibility = Visibility.public
    version: str = Field("1.0.0", pattern=r"^\d+\.\d+\.\d+$")


class AgentUpdate(BaseModel):
    summary: str | None = Field(None, max_length=280)
    description: str | None = None
    endpoint: HttpUrl | None = None
    protocol: AgentProtocol | None = None
    auth: AuthType | None = None
    scopes: list[str] | None = None
    skills: list[AgentSkillRef] | None = None
    tags: list[str] | None = None
    visibility: Visibility | None = None
    version: str | None = Field(None, pattern=r"^\d+\.\d+\.\d+$")


class Agent(ResourceBase):
    kind: Literal[ResourceKind.agent] = ResourceKind.agent
    endpoint: HttpUrl
    protocol: AgentProtocol = AgentProtocol.a2a
    auth: AuthType = AuthType.entra
    scopes: list[str] = Field(default_factory=list)
    skills: list[AgentSkillRef] = Field(default_factory=list)


# --------------------------------------------------------------------------- #
# MCP servers
# --------------------------------------------------------------------------- #
class MCPTransport(str, Enum):
    streamable_http = "streamable_http"
    stdio = "stdio"
    websocket = "websocket"


class MCPToolRef(BaseModel):
    name: str
    description: str = ""


class MCPServerCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    summary: str = Field(..., max_length=280)
    description: str = ""
    url: HttpUrl
    transport: MCPTransport = MCPTransport.streamable_http
    auth: AuthType = AuthType.entra
    scopes: list[str] = Field(default_factory=list)
    tools: list[MCPToolRef] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    visibility: Visibility = Visibility.public
    version: str = Field("1.0.0", pattern=r"^\d+\.\d+\.\d+$")


class MCPServerUpdate(BaseModel):
    summary: str | None = Field(None, max_length=280)
    description: str | None = None
    url: HttpUrl | None = None
    transport: MCPTransport | None = None
    auth: AuthType | None = None
    scopes: list[str] | None = None
    tools: list[MCPToolRef] | None = None
    tags: list[str] | None = None
    visibility: Visibility | None = None
    version: str | None = Field(None, pattern=r"^\d+\.\d+\.\d+$")


class MCPServer(ResourceBase):
    kind: Literal[ResourceKind.mcp_server] = ResourceKind.mcp_server
    url: HttpUrl
    transport: MCPTransport = MCPTransport.streamable_http
    auth: AuthType = AuthType.entra
    scopes: list[str] = Field(default_factory=list)
    tools: list[MCPToolRef] = Field(default_factory=list)


# --------------------------------------------------------------------------- #
# Skills
# --------------------------------------------------------------------------- #
class SkillKind(str, Enum):
    prompt = "prompt"        # declarative prompt agent (YAML)
    tool = "tool"            # function-tool contract
    workflow = "workflow"    # declarative workflow (YAML)


class SkillCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    summary: str = Field(..., max_length=280)
    description: str = ""
    skill_kind: SkillKind = SkillKind.prompt
    spec: str = Field(..., description="YAML or text definition of the skill.")
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    visibility: Visibility = Visibility.public
    version: str = Field("1.0.0", pattern=r"^\d+\.\d+\.\d+$")


class SkillUpdate(BaseModel):
    summary: str | None = Field(None, max_length=280)
    description: str | None = None
    skill_kind: SkillKind | None = None
    spec: str | None = None
    inputs: list[str] | None = None
    outputs: list[str] | None = None
    tags: list[str] | None = None
    visibility: Visibility | None = None
    version: str | None = Field(None, pattern=r"^\d+\.\d+\.\d+$")


class Skill(ResourceBase):
    kind: Literal[ResourceKind.skill] = ResourceKind.skill
    skill_kind: SkillKind = SkillKind.prompt
    spec: str = ""
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)


# --------------------------------------------------------------------------- #
# Generic API envelopes
# --------------------------------------------------------------------------- #
T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    """A page of search results."""

    items: list[T]
    count: int
    total: int


class HealthStatus(BaseModel):
    status: Literal["ok", "degraded"] = "ok"
    store: str
    auth_mode: str
    version: str


CatalogResource = Annotated[Agent | MCPServer | Skill, Field(discriminator="kind")]
