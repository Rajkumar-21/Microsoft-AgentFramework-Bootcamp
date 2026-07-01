# Module 06: Streaming Responses

> **Scenario — Helios SRE Live Postmortem Writer.** Streams a structured incident
> postmortem token-by-token onto a dashboard and measures **time-to-first-token
> (TTFT)** — while keeping multi-turn memory via a shared thread.

## Learning Objectives
- Use `agent.run_stream()` for real-time response output
- Process async chunks as they arrive (`async for update in ...`)
- Measure time-to-first-token to reason about perceived latency
- Combine streaming with thread memory for stateful follow-ups

## Key Concepts
- **`agent.run_stream(message)`** - async generator of incremental updates
- **`update.text`** - text content of each chunk (concatenate for full text)
- **`flush=True`** - force chunks to render immediately in a terminal
- **TTFT** - time to the first visible character; the real latency users feel

## Exercises
1. Compare wall-clock time of `run()` vs. `run_stream()` for the same prompt
2. Add a cancel-after-N-chars guard to stop a runaway response
3. Stream a follow-up turn on the same thread and confirm memory is retained

## How to Run
```bash
cd modules/06_streaming_responses
python main.py
```

## Files
- `main.py` - Streaming postmortem writer with TTFT measurement
