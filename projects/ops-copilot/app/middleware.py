"""Cross-cutting middleware: audit logging and simple PII redaction.

Agent middleware in the Agent Framework are async callables ``(context, next)``
that wrap each agent invocation. They are passed as a **list** to the agent.
"""

from __future__ import annotations

import logging
import re
from typing import Any, Awaitable, Callable

logger = logging.getLogger("ops_copilot.audit")

_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_IP = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")


def _redact(text: str) -> str:
    text = _EMAIL.sub("[redacted-email]", text)
    text = _IP.sub("[redacted-ip]", text)
    return text


async def audit_middleware(
    context: Any, next: Callable[[Any], Awaitable[None]]
) -> None:
    """Log each agent call with redacted input for an audit trail."""
    agent_name = getattr(getattr(context, "agent", None), "name", "agent")
    try:
        messages = getattr(context, "messages", None) or []
        preview = " ".join(getattr(m, "text", "") for m in messages)[:200]
        logger.info("→ %s invoked: %s", agent_name, _redact(preview))
    except Exception:  # never let auditing break the run
        logger.info("→ %s invoked", agent_name)

    await next(context)

    logger.info("← %s completed", agent_name)
