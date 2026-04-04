# Module 16: Sub-Workflows

## Learning Objectives
- Create nested workflows (workflow within a workflow)
- Use `WorkflowExecutor` for sub-workflow execution
- Build custom `Executor` classes with `@handler` decorator
- Control flow with `WorkflowContext` methods (yield_output, send_message, add_event)

## Key Concepts
- **`WorkflowExecutor`** - Wraps a workflow as an executor in a parent workflow
- **`Executor`** base class - Custom executor with handler methods
- **`@handler`** decorator - Marks methods as message handlers
- **`WorkflowContext`** - `yield_output()`, `send_message()`, `add_event()`
- **`WorkflowEvent`** - Custom events for flow control

## Exercises
1. Build a parent orchestrator with child sub-workflows
2. Create custom executors with event-driven handlers
3. Implement data transformation pipeline with sub-workflows

## Files
- `main.py` - Sub-workflow: orchestrator with nested workflows
