# Module 11: Workflows - Sequential

## Learning Objectives
- Build linear multi-agent workflows with WorkflowBuilder
- Chain agents in sequence: A → B → C → D
- Understand workflow execution flow and data passing
- Use `set_start_executor()` and `add_edge()` methods

## Key Concepts
- **`WorkflowBuilder`** - Fluent API for building agent workflows
- **`set_start_executor(agent)`** - Define the first agent in the pipeline
- **`add_edge(from, to)`** - Connect agents in sequence
- **`.build()`** - Compile the workflow
- **`workflow.run(input)`** - Execute the workflow

## Workflow Diagram
```
Writer → Reviewer → Editor → Publisher
```

## Exercises
1. Build a content creation pipeline (Writer → Reviewer → Publisher)
2. Build a data processing pipeline (Extract → Transform → Load)
3. Add error handling between workflow steps

## Files
- `main.py` - Sequential workflow: content creation pipeline
