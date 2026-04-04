# Module 10: Middleware System

## Learning Objectives
- Understand agent-level vs run-level middleware
- Create custom middleware with `AgentMiddleware`
- Use `@chat_middleware` and `@function_middleware` decorators
- Implement logging, security, rate-limiting middleware
- Apply middleware to specific runs or all runs

## Key Concepts
- **Agent-level middleware** - Applied to ALL runs (set at creation)
- **Run-level middleware** - Applied to specific runs only
- **`AgentMiddleware`** class - Base class with `process()` method
- **`@chat_middleware`** - Decorator for chat request/response interception
- **`@function_middleware`** - Decorator for tool call interception
- **`FunctionInvocationContext`** - Context for function middleware

## Middleware Flow
```
User Request → Chat Middleware → Agent → Function Middleware → Tool
                                   ↓
                            Chat Middleware → Response
```

## Exercises
1. Create a logging middleware that tracks all agent calls
2. Create a security middleware that filters sensitive inputs
3. Create a performance monitoring middleware
4. Apply middleware at agent-level and run-level

## Files
- `main.py` - Middleware examples (agent-level and run-level)
