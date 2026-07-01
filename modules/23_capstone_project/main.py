"""
Module 23: Capstone Project
Enterprise Knowledge Assistant - Multi-Agent System

Combines: Providers, Tools, Threads, Streaming, Structured Outputs,
Middleware, Workflows (Handoff), Agent-as-Tool, Observability
"""

import asyncio
import os

from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import HandoffBuilder

from middleware import LoggingMiddleware, SecurityMiddleware, tool_audit_middleware
from tools import (
    create_support_ticket,
    get_system_status,
    run_code_analysis,
    search_knowledge_base,
)


async def main():
    chat_client = OpenAIChatClient(
        model=os.environ["AZURE_OPENAI_MODEL"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )

    # Shared middleware pipeline
    shared_middleware = [LoggingMiddleware(), SecurityMiddleware(), tool_audit_middleware]

    # === Agent Definitions ===

    # Triage Agent
    triage = chat_client.as_agent(
        name="TriageAgent",
        instructions=(
            "You are a triage agent. Classify user requests into:\n"
            "- 'research': For information lookup, analysis, trends\n"
            "- 'code': For code help, reviews, debugging\n"
            "- 'support': For system issues, tickets, account help\n\n"
            "Include the category keyword in your response."
        ),
        middleware=shared_middleware,
    )

    # Research Agent (with knowledge base search)
    research_agent = chat_client.as_agent(
        name="ResearchAgent",
        instructions=(
            "You are a research assistant. Search the knowledge base "
            "and provide comprehensive, well-sourced answers."
        ),
        tools=[search_knowledge_base],
        middleware=shared_middleware,
    )

    # Code Agent (with code analysis)
    code_agent = chat_client.as_agent(
        name="CodeAgent",
        instructions=(
            "You are a code assistant. Help with code reviews, "
            "debugging, and best practices. Use the analysis tool."
        ),
        tools=[run_code_analysis],
        middleware=shared_middleware,
    )

    # Support Agent (with ticket creation + system status)
    support_agent = chat_client.as_agent(
        name="SupportAgent",
        instructions=(
            "You are a support agent. Help users with system issues, "
            "create tickets, and check system status."
        ),
        tools=[create_support_ticket, get_system_status],
        middleware=shared_middleware,
    )

    # Final Response Formatter
    formatter = chat_client.as_agent(
        name="ResponseFormatter",
        instructions=(
            "Format the specialist's response into a polished, "
            "user-friendly message. Add a reference ID and ask "
            "if the user needs further help."
        ),
        middleware=shared_middleware,
    )

    # === Build Handoff Workflow (LLM-driven routing) ===
    workflow = (
        HandoffBuilder(
            name="EnterpriseKnowledgeAssistant",
            participants=[triage, research_agent, code_agent, support_agent, formatter],
        )
        .with_start_agent(triage)
        .add_handoff(triage, [research_agent, code_agent, support_agent])
        .add_handoff(research_agent, [formatter])
        .add_handoff(code_agent, [formatter])
        .add_handoff(support_agent, [formatter])
        .build()
    )

    # === Run Tests ===
    test_queries = [
        "I need to research the latest API deployment best practices",
        "Can you review this code: def calc(x): return eval(x)",
        "My system is running slow, can you check the status and create a ticket?",
    ]

    for query in test_queries:
        print(f"\n{'='*70}")
        print(f"🧑 User: {query}")
        print(f"{'='*70}")

        events = await workflow.run(query)
        for output in events.get_outputs():
            print(f"\n🤖 Assistant:\n{output}")

    print(f"\n{'='*70}")
    print("✅ Capstone project complete!")
    print("Patterns used: Triage, Handoff, Function Tools, Middleware,")
    print("  Observability, Security, HandoffBuilder, Multi-Agent")


if __name__ == "__main__":
    asyncio.run(main())
