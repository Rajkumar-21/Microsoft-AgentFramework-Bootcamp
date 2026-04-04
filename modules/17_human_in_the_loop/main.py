"""
Module 17: Human-in-the-Loop
Approval gates for agent tool execution.

Two approaches shown:
  1. Built-in: @tool(approval_mode="always_require") — SDK-managed approval.
  2. Custom:   @function_middleware to implement bespoke approval logic.

This example uses the custom middleware approach for fine-grained control.
"""

import asyncio
import os
from typing import Annotated

from pydantic import Field

from agent_framework import function_middleware, tool
from agent_framework.openai import OpenAIChatClient


# ---------------------------------------------------------------------------
# Tools that may require approval
# ---------------------------------------------------------------------------
@tool
def send_email(
    to: Annotated[str, Field(description="Recipient email address")],
    subject: Annotated[str, Field(description="Email subject line")],
    body: Annotated[str, Field(description="Email body content")],
) -> str:
    """Send an email to the specified recipient."""
    # In production, actually send the email
    return f"Email sent to {to} with subject: {subject}"


@tool
def delete_record(
    record_id: Annotated[str, Field(description="ID of the record to delete")],
) -> str:
    """Delete a record from the database."""
    return f"Record {record_id} deleted successfully."


@tool
def search_database(
    query: Annotated[str, Field(description="Search query")],
) -> str:
    """Search the database for matching records."""
    return f"Found 3 records matching '{query}': [R001, R002, R003]"


# ---------------------------------------------------------------------------
# Human-in-the-loop middleware (custom approval gate)
# ---------------------------------------------------------------------------
@function_middleware
async def approval_gate(context, call_next):
    """Require human approval for destructive operations."""
    dangerous_functions = {"send_email", "delete_record"}

    if context.function.name in dangerous_functions:
        print(f"\n\u26a0\ufe0f  APPROVAL REQUIRED")
        print(f"  Function: {context.function.name}")
        print(f"  Arguments: {context.arguments}")

        # In a real application this would be a UI prompt or API call
        approval = input("  Approve? (y/n): ").strip().lower()

        if approval != "y":
            print("  \u274c Action REJECTED by user.")
            context.result = f"Action '{context.function.name}' was rejected by the user."
            return

        print("  \u2705 Action APPROVED by user.")

    await call_next()


async def main():
    # --- Azure OpenAI client ---
    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )

    agent = client.as_agent(
        name="SafeAgent",
        instructions=(
            "You are a helpful assistant with access to email, database search, "
            "and record deletion. Use these tools to help the user. "
            "Always confirm important actions with the user."
        ),
        tools=[send_email, delete_record, search_database],
        middleware=[approval_gate],
    )

    # Test: Safe action (no approval needed)
    print("=== Safe Action (Search) ===")
    result = await agent.run("Search the database for 'customer reports'")
    print(f"Agent: {result.text}\n")

    # Test: Dangerous actions (approval required)
    print("=== Dangerous Actions (Approval Required) ===")
    result = await agent.run("Send an email to team@example.com about the quarterly review")
    print(f"Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
