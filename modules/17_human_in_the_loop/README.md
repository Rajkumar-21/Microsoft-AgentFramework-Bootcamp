# Module 17: Human-in-the-Loop

## Learning Objectives
- Implement approval gates before tool execution
- Use `FunctionInvocationContext` for function approval/rejection
- Build human confirmation workflows for critical actions
- Add safety controls to agent tool calls

## Key Concepts
- **`@function_middleware`** - Intercept tool calls before execution
- **`FunctionInvocationContext`** - Access function name, args, approve/reject
- **Approval patterns** - Human confirms before agent executes actions
- **Safety guardrails** - Block dangerous operations automatically

## Exercises
1. Create an approval gate for database write operations
2. Build a confirmation prompt before sending emails
3. Implement automatic rejection of unsafe tool calls

## Files
- `main.py` - Human-in-the-loop approval gate example
