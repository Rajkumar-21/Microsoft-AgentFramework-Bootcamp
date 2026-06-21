# Module 05: Conversation Threads

> **Scenario — Summit Bank Mortgage Pre-Qualification Advisor.** A multi-turn advisor
> that remembers income, down payment, and target price across the interview — then
> summarizes and pre-qualifies. The module runs the same turns *with* and *without* a
> thread so the difference is unmistakable.

## Learning Objectives
- Create persistent conversation threads for multi-turn dialogue
- Use `agent.get_new_thread()` (synchronous) for conversation context
- Pass `thread=` to maintain conversation state across `run()` calls
- See how omitting the thread makes the agent stateless

## Key Concepts
- **`agent.get_new_thread()`** - create a new thread (sync — do not await)
- **`thread=thread`** in `agent.run()` - carry history forward
- **One thread = one conversation** - separate users get separate threads
- **Stateless by default** - no thread means no memory

## Exercises
1. Add a turn that contradicts an earlier one; watch the agent reconcile it
2. Reuse one thread across two different applicants (anti-pattern — observe leakage)
3. Print `response.messages` to inspect accumulated history

## How to Run
```bash
cd modules/05_conversation_threads
python main.py
```

## Files
- `main.py` - Mortgage advisor demonstrating threaded vs. stateless runs
