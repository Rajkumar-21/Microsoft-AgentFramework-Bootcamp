"""CLI entry point: run the incident workflow once, with HITL approvals.

Usage:
    python -m app.run "CPU on web-prod-3 is at 98% for 10 minutes"
"""

from __future__ import annotations

import asyncio
import os
import sys

from dotenv import load_dotenv

from .registry import self_register
from .workflow import build_incident_workflow


def _setup_observability() -> None:
    conn = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if not conn:
        return
    try:
        from agent_framework.observability import configure_otel_providers

        configure_otel_providers()
    except Exception:
        pass


async def _handle_approvals(workflow, events):
    """Prompt the operator to approve any pending tool calls, then resume."""
    responses = {}
    for event in events:
        if getattr(event, "type", None) != "request_info":
            continue
        data = getattr(event, "data", None)
        if getattr(data, "type", None) != "function_approval_request":
            continue
        func = getattr(data, "function_call", None)
        name = getattr(func, "name", "action")
        answer = input(f"\n[APPROVAL NEEDED] Allow '{name}'? [y/N] ").strip().lower()
        responses[event.request_id] = data.to_function_approval_response(
            approved=answer == "y"
        )
    if responses:
        async for ev in workflow.run_stream(responses=responses):
            _print_event(ev)


def _print_event(event) -> None:
    text = getattr(event, "text", None)
    if text:
        print(text, end="", flush=True)


async def main(alert: str) -> None:
    load_dotenv()
    _setup_observability()
    await self_register()

    workflow = await build_incident_workflow()
    print(f"\n=== Incident: {alert} ===\n")

    pending = []
    async for event in workflow.run_stream(alert):
        _print_event(event)
        if getattr(event, "type", None) == "request_info":
            pending.append(event)

    await _handle_approvals(workflow, pending)
    print("\n\n=== Incident handling complete ===")


if __name__ == "__main__":
    alert = sys.argv[1] if len(sys.argv) > 1 else "High latency on checkout-api"
    asyncio.run(main(alert))
