# 05 – Conversation Threads

!!! abstract "Module Goals"
    Create multi-turn conversations with persistent context using threads.

## Key Concepts

| Concept | Description |
|---------|-------------|
| `agent.get_new_thread()` | Create a new conversation thread |
| `thread=thread` | Pass thread to `run()` for context |
| `thread.conversation_id` | Unique ID for the thread |
| Multi-turn | Agent remembers previous messages |

## How Threads Work

```mermaid
sequenceDiagram
    participant User
    participant Agent
    participant Thread

    User->>Agent: run("I'm going to Japan", thread)
    Agent->>Thread: Store message + response
    Agent-->>User: "Great! Japan is wonderful..."

    User->>Agent: run("What about Tokyo?", thread)
    Agent->>Thread: Retrieve context (knows about Japan)
    Agent-->>User: "In Tokyo, you should visit..."
```

## Code

```python title="modules/05_conversation_threads/main.py"
--8<-- "modules/05_conversation_threads/main.py"
```

## Run It

```bash
uv run python modules/05_conversation_threads/main.py
```

## Exercises

- [ ] Create a multi-turn travel planning conversation
- [ ] Compare responses **with** and **without** threads
- [ ] Save and display the thread ID

!!! tip "Next"
    [06 – Streaming Responses](06-streaming-responses.md)
