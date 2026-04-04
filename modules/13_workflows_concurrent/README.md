# Module 13: Workflows - Concurrent

## Learning Objectives
- Run multiple agents in parallel with ConcurrentBuilder
- Collect outputs from all parallel agents
- Understand when to use concurrent vs sequential patterns

## Key Concepts
- **`ConcurrentBuilder`** - Build parallel agent execution
- **`.participants([agent1, agent2, ...])`** - Define parallel agents
- **`events.get_outputs()`** - Collect all parallel results
- **Fan-out pattern** - Same input processed by multiple specialists

## Exercises
1. Build a concurrent research workflow (multiple researchers)
2. Compare concurrent vs sequential performance
3. Aggregate results from parallel agents

## Files
- `main.py` - Concurrent workflow: parallel research agents
