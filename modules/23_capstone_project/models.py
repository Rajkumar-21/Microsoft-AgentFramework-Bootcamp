"""
Capstone: Pydantic models for structured outputs.
"""

from pydantic import BaseModel, ConfigDict


class TriageResult(BaseModel):
    """Triage agent's classification of user request."""

    model_config = ConfigDict(extra="forbid")

    category: str  # "research", "code", "support"
    confidence: float
    reasoning: str
    initial_response: str


class ResearchReport(BaseModel):
    """Structured research output."""

    model_config = ConfigDict(extra="forbid")

    topic: str
    summary: str
    key_findings: list[str]
    sources: list[str]
    confidence: float


class CodeReview(BaseModel):
    """Structured code review output."""

    model_config = ConfigDict(extra="forbid")

    language: str
    issues_found: list[str]
    suggestions: list[str]
    overall_quality: str  # "good", "needs_improvement", "critical"
    refactored_code: str


class SupportTicket(BaseModel):
    """Structured support ticket output."""

    model_config = ConfigDict(extra="forbid")

    ticket_id: str
    category: str
    priority: str  # "low", "medium", "high", "critical"
    resolution: str
    follow_up_required: bool
