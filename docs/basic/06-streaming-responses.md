# 06 – Streaming Responses

!!! abstract "Module Goals"
    Use `run_stream()` for real-time response output as the agent generates text.

## Key Concepts

| Concept | Description |
|---------|-------------|
| `agent.run_stream()` | Returns async iterator of chunks |
| `chunk.text` | Text content of each chunk |
| `async for` | Iterate over streaming chunks |
| Real-time UX | Display tokens as they arrive |

## Streaming vs Non-Streaming

| Aspect | `run()` | `run_stream()` |
|--------|---------|----------------|
| Latency to first token | High (waits for full response) | Low (returns immediately) |
| UX | Shows complete response at once | Typewriter effect |
| Use case | Short answers, structured outputs | Long responses, stories, chat UIs |

## Code

```python title="modules/06_streaming_responses/main.py"
--8<-- "modules/06_streaming_responses/main.py"
```

## Run It

```bash
uv run python modules/06_streaming_responses/main.py
```

## Exercises

- [ ] Stream a long response and display in real-time
- [ ] Compare perceived latency: streaming vs non-streaming
- [ ] Combine streaming with conversation threads

!!! success "Basic Complete!"
    You've finished all 6 Basic modules. Move on to [Intermediate →](../intermediate/index.md)
