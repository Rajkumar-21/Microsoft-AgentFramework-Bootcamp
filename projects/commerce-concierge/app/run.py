"""CLI entry point: run the concierge once with streaming output.

Usage:
    python -m app.run "I need a waterproof jacket for hiking under $150"
"""

from __future__ import annotations

import asyncio
import os
import sys

from dotenv import load_dotenv

from .registry import self_register
from .workflow import build_concierge_workflow


def _setup_observability() -> None:
    if not os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
        return
    try:
        from agent_framework.observability import configure_otel_providers

        configure_otel_providers()
    except Exception:
        pass


async def main(message: str) -> None:
    load_dotenv()
    _setup_observability()
    await self_register()

    workflow = await build_concierge_workflow()
    print(f"\n=== Shopper: {message} ===\n")

    async for event in workflow.run_stream(message):
        text = getattr(event, "text", None)
        if text:
            print(text, end="", flush=True)

    print("\n\n=== Done ===")


if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Recommend a waterproof hiking jacket under $150"
    asyncio.run(main(msg))
