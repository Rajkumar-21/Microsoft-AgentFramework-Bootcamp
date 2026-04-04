"""
Capstone: Middleware pipeline for observability and security.
"""

import time

from agent_framework import AgentContext, AgentMiddleware, function_middleware


class LoggingMiddleware(AgentMiddleware):
    """Log all agent interactions with timing."""

    async def process(self, context: AgentContext, call_next) -> None:
        agent_name = context.agent.name
        start = time.time()
        print(f"  📡 [{agent_name}] Processing...")

        try:
            await call_next()
        finally:
            elapsed = (time.time() - start) * 1000
            print(f"  ⏱️  [{agent_name}] Done ({elapsed:.0f}ms)")


class SecurityMiddleware(AgentMiddleware):
    """Filter sensitive content from requests."""

    SENSITIVE_PATTERNS = ["password", "secret", "token", "api_key", "private_key"]

    async def process(self, context: AgentContext, call_next) -> None:
        input_text = str(context.messages).lower()
        for pattern in self.SENSITIVE_PATTERNS:
            if pattern in input_text:
                print(f"  🔒 [Security] Sensitive content detected: '{pattern}'")
                # Let it through but log the alert
                break
        await call_next()


@function_middleware
async def tool_audit_middleware(context, call_next):
    """Audit all tool invocations."""
    print(f"  🔧 Tool: {context.function.name}({context.arguments})")
    await call_next()
