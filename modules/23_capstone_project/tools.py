"""
Capstone: Custom function tools.
"""

from datetime import datetime, timezone
from typing import Annotated

from pydantic import Field

from agent_framework import tool


@tool
def search_knowledge_base(
    query: Annotated[str, Field(description="Search query for the knowledge base")],
) -> str:
    """Search the internal knowledge base for relevant articles."""
    # Simulated knowledge base
    articles = {
        "password reset": "KB001: Go to Settings > Security > Reset Password",
        "billing": "KB002: Billing inquiries can be handled at billing.example.com",
        "api": "KB003: API documentation at docs.example.com/api",
        "deployment": "KB004: Deployment guide at docs.example.com/deploy",
    }
    results = []
    for key, val in articles.items():
        if key in query.lower():
            results.append(val)
    return f"Found {len(results)} articles: {'; '.join(results)}" if results else "No articles found."


@tool
def create_support_ticket(
    title: Annotated[str, Field(description="Ticket title")],
    priority: Annotated[str, Field(description="Priority: low, medium, high, critical")],
    description: Annotated[str, Field(description="Ticket description")],
) -> str:
    """Create a support ticket in the ticketing system."""
    ticket_id = f"TKT-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    return f"Ticket created: {ticket_id} | Priority: {priority} | Title: {title}"


@tool
def run_code_analysis(
    code: Annotated[str, Field(description="Code snippet to analyze")],
    language: Annotated[str, Field(description="Programming language")],
) -> str:
    """Run static analysis on a code snippet."""
    # Simulated analysis
    issues = []
    if "eval(" in code:
        issues.append("SECURITY: Dangerous use of eval()")
    if "except:" in code:
        issues.append("QUALITY: Bare except clause - catch specific exceptions")
    if "TODO" in code:
        issues.append("CLEANUP: Unresolved TODO comments found")

    if not issues:
        issues.append("No issues found - code looks clean!")

    return f"Analysis ({language}): {'; '.join(issues)}"


@tool
def get_system_status() -> str:
    """Check the status of all systems."""
    return (
        "System Status:\n"
        "- API Gateway: ✅ Healthy\n"
        "- Database: ✅ Healthy\n"
        "- Cache: ⚠️ High latency (150ms)\n"
        "- Queue: ✅ Healthy\n"
        f"- Last checked: {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}"
    )
