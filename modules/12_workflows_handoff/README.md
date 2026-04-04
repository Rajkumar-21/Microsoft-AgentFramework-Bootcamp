# Module 12: Workflows - Handoff

## Learning Objectives
- Build conditional routing workflows with handoff patterns
- Use `add_edge(from, to, condition=func)` for branching logic
- Implement triage-based routing (customer support pattern)
- Converge multiple branches back to a single agent

## Key Concepts
- **Conditional edges** - `add_edge(triage, agent, condition=check_fn)`
- **Triage pattern** - First agent classifies, then routes to specialist
- **Structured outputs** - Use Pydantic for routing decisions
- **Convergence** - Multiple branches merge to final agent

## Workflow Diagram
```
                ┌→ RefundAgent ──┐
User → Triage ──┤→ OrderAgent ───┤→ FinalResponse
                └→ SupportAgent ─┘
```

## Exercises
1. Build a customer support handoff workflow
2. Add custom routing conditions
3. Handle edge cases (unknown categories)

## Files
- `main.py` - Handoff workflow: customer support routing
