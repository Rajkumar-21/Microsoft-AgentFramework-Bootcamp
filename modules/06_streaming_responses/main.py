"""
Module 06 — Streaming Responses
===============================

Scenario: Helios SRE — Live Incident Postmortem Writer
------------------------------------------------------
After an outage, the on-call engineer needs a postmortem *now*. Instead of
waiting for the whole document, we stream it token-by-token so it renders in
real time on the incident dashboard — and we measure time-to-first-token (TTFT),
a metric that matters for perceived latency.

The mechanism is `agent.run_stream(...)`:
  * It is an async generator — iterate with `async for update in ...`.
  * Each `update.text` is an incremental chunk; concatenate them for the full text.
  * Combine with a thread to stream *and* keep multi-turn memory.
"""

import asyncio
import os
import time

from agent_framework.azure import AzureOpenAIChatClient


WRITER_INSTRUCTIONS = """\
You are an SRE postmortem writer. Produce blameless, structured incident
postmortems with these sections: Summary, Impact, Timeline, Root Cause,
Resolution, and Action Items. Be specific and concise."""

INCIDENT_BRIEF = (
    "Write a postmortem for INC-4821: the checkout service returned 503s for "
    "23 minutes after a deploy exhausted the database connection pool. "
    "Rolled back to restore service. ~8% of checkout traffic affected."
)


def build_client() -> AzureOpenAIChatClient:
    deployment = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME") or os.environ["AZURE_OPENAI_MODEL"]
    return AzureOpenAIChatClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        deployment_name=deployment,
    )


async def stream_postmortem(agent, thread) -> str:
    """Stream a response, print it live, and report TTFT. Returns full text."""
    print("Agent: ", end="", flush=True)
    started = time.perf_counter()
    ttft: float | None = None
    chunks: list[str] = []

    async for update in agent.run_stream(INCIDENT_BRIEF, thread=thread):
        if update.text:
            if ttft is None:
                ttft = time.perf_counter() - started
            chunks.append(update.text)
            print(update.text, end="", flush=True)

    full = "".join(chunks)
    print(
        f"\n\n[streamed {len(full)} chars · "
        f"time-to-first-token {ttft * 1000:.0f} ms]"
        if ttft is not None
        else "\n\n[no content streamed]"
    )
    return full


async def main() -> None:
    client = build_client()
    agent = client.create_agent(name="PostmortemWriter", instructions=WRITER_INSTRUCTIONS)
    thread = agent.get_new_thread()

    print("=" * 64)
    print("  Streaming postmortem for INC-4821")
    print("=" * 64)
    await stream_postmortem(agent, thread)

    # Follow-up turn — the thread keeps context, and we stream again.
    print("\n" + "=" * 64)
    print("  Follow-up (same thread): extract just the action items")
    print("=" * 64)
    print("Agent: ", end="", flush=True)
    async for update in agent.run_stream(
        "List only the action items as a numbered checklist with owners.", thread=thread
    ):
        if update.text:
            print(update.text, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(main())
