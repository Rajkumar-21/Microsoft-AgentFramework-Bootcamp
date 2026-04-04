"""
Module 16: Sub-Workflows
Nested workflows — a parent workflow that orchestrates child workflows.

Uses the low-level WorkflowBuilder with custom Executor classes for
full control over message routing, and WorkflowExecutor to embed a
child workflow inside the parent.
"""

import asyncio
import os

from agent_framework import (
    Executor,
    WorkflowBuilder,
    WorkflowContext,
    WorkflowExecutor,
    handler,
)
from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import SequentialBuilder


# ---------------------------------------------------------------------------
# Custom Executor: Orchestrator that triggers sub-workflows
# ---------------------------------------------------------------------------
class TextProcessingOrchestrator(Executor):
    """Orchestrator that sends work to sub-workflows and collects results."""

    def __init__(self):
        super().__init__(id="orchestrator")
        self.results: list[str] = []
        self.tasks_sent = 0

    @handler
    async def handle_input(self, message: str, ctx: WorkflowContext) -> None:
        """Handle initial input — send to processing sub-workflow."""
        print("[Orchestrator] Received input, sending to processing sub-workflow...")
        self.tasks_sent += 1
        await ctx.send_message(message, target_id="processor")

    @handler
    async def handle_result(self, message: str, ctx: WorkflowContext) -> None:
        """Handle results from sub-workflow."""
        self.results.append(message)
        print(
            f"[Orchestrator] Received processed result "
            f"({len(self.results)}/{self.tasks_sent})"
        )

        if len(self.results) >= self.tasks_sent:
            # All tasks complete — yield final output
            final = "\n\n---\n\n".join(self.results)
            await ctx.yield_output(final)


async def main():
    # --- Azure OpenAI client ---
    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )

    # Child workflow agents
    analyzer = client.as_agent(
        name="Analyzer",
        instructions=(
            "Analyze the given text. Identify key themes, sentiment, "
            "and main arguments. Be concise."
        ),
    )

    summarizer = client.as_agent(
        name="Summarizer",
        instructions="Take the analysis and create a brief executive summary (3-4 sentences max).",
    )

    # Build child sub-workflow: Analyzer → Summarizer (sequential)
    child_workflow = SequentialBuilder(
        participants=[analyzer, summarizer],
    ).build()

    # Create orchestrator and workflow executor
    orchestrator = TextProcessingOrchestrator()
    workflow_executor = WorkflowExecutor(child_workflow, id="processor")

    # Build parent workflow: Orchestrator ↔ Sub-Workflow
    parent_workflow = (
        WorkflowBuilder(start_executor=orchestrator)
        .add_edge(orchestrator, workflow_executor)
        .add_edge(workflow_executor, orchestrator)
        .build()
    )

    # Execute
    print("=== Sub-Workflow: Text Processing Pipeline ===\n")
    result = await parent_workflow.run(
        "The rapid advancement of AI agents is transforming how businesses operate. "
        "Companies are adopting multi-agent systems for customer service, data analysis, "
        "and software development. However, concerns about reliability, security, and "
        "job displacement continue to spark debate among industry leaders and policymakers."
    )

    for output in result.get_outputs():
        print(f"\nFinal Output:\n{output}")


if __name__ == "__main__":
    asyncio.run(main())
