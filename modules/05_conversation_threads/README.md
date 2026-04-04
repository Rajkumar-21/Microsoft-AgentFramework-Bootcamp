# Module 05: Conversation Threads

## Learning Objectives
- Create persistent conversation threads for multi-turn dialogue
- Use `agent.get_new_thread()` for conversation context
- Pass `thread=` parameter to maintain conversation state
- Understand thread IDs for conversation resumption

## Key Concepts
- **`agent.get_new_thread()`** - Create a new conversation thread
- **`thread=thread`** parameter in `agent.run()` - Maintain context
- **`thread.conversation_id`** - Unique thread identifier
- **Multi-turn conversations** - Agent remembers previous messages

## Exercises
1. Create a multi-turn conversation with context retention
2. Compare responses with and without threads
3. Save and display thread IDs

## Files
- `main.py` - Multi-turn conversation with threads
