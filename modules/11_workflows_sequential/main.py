"""
Module 11: Workflows — Sequential
Build linear multi-agent pipelines.

SequentialBuilder(participants=[a, b, c]).build() creates a workflow where
each agent’s output becomes the next agent’s input, in order.
"""

import asyncio
import os

from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import SequentialBuilder


async def main():
    # --- Azure OpenAI client ---
    client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )

    # Create specialist agents
    writer = client.as_agent(
        name="Writer",
        instructions=(
            "You are a content writer. Write a short blog post (3-4 paragraphs) "
            "based on the given topic. Be creative and engaging."
        ),
    )

    reviewer = client.as_agent(
        name="Reviewer",
        instructions=(
            "You are a content reviewer. Review the blog post provided. "
            "Give specific feedback on clarity, tone, and structure. "
            "Then provide the improved version."
        ),
    )

    publisher = client.as_agent(
        name="Publisher",
        instructions=(
            "You are a publisher. Take the reviewed content and format it "
            "for publication. Add a compelling title, meta description, "
            "and relevant tags. Output the final formatted version."
        ),
    )

    # Build sequential workflow: Writer → Reviewer → Publisher
    workflow = SequentialBuilder(
        participants=[writer, reviewer, publisher],
    ).build()

    # Execute the workflow
    print("=== Content Creation Pipeline ===\n")
    result = await workflow.run("Write a blog post about the future of AI agents in 2025")

    # Get the final output(s)
    for output in result.get_outputs():
        print(f"--- Final Published Content ---\n{output}")


if __name__ == "__main__":
    asyncio.run(main())
