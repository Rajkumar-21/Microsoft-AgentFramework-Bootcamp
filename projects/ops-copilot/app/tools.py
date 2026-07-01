"""Function tools used by the Ops Copilot agents."""

from __future__ import annotations

import random
from typing import Annotated

from agent_framework import tool
from pydantic import Field


@tool
def get_metric(
    host: Annotated[str, Field(description="Host or service name.")],
    metric: Annotated[str, Field(description="Metric name, e.g. cpu, memory.")],
) -> str:
    """Return the latest value for a host metric (simulated)."""
    value = round(random.uniform(40, 99), 1)
    return f"{metric} on {host} is currently {value}%."


@tool
def lookup_runbook(
    symptom: Annotated[str, Field(description="Observed symptom or alert text.")],
) -> str:
    """Look up the recommended runbook for a symptom (simulated KB)."""
    kb = {
        "cpu": "RB-101: Scale out the affected tier, then investigate hot paths.",
        "memory": "RB-102: Recycle the worker, capture a heap dump, check for leaks.",
        "latency": "RB-103: Check downstream dependencies and connection pools.",
    }
    for key, runbook in kb.items():
        if key in symptom.lower():
            return runbook
    return "RB-001: Triage manually; no specific runbook matched."


@tool(approval_mode="always_require")
def restart_service(
    host: Annotated[str, Field(description="Host to restart.")],
    service: Annotated[str, Field(description="Service name to restart.")],
) -> str:
    """Restart a production service. Requires human approval before running."""
    return f"Service '{service}' on '{host}' was restarted successfully."
