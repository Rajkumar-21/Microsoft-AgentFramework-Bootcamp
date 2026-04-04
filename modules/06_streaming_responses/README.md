# Module 06: Streaming Responses

## Learning Objectives
- Use `agent.run_stream()` for real-time response output
- Process async chunks as they arrive
- Understand streaming vs non-streaming trade-offs

## Key Concepts
- **`agent.run_stream(message)`** - Returns async iterator of chunks
- **`chunk.text`** - Text content of each chunk
- **`async for`** - Iterate over streaming chunks
- **Real-time UX** - Display responses as they generate

## Exercises
1. Stream a long response and display in real-time
2. Compare latency: streaming vs non-streaming
3. Combine streaming with conversation threads

## Files
- `main.py` - Streaming response examples
