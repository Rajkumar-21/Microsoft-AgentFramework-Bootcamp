# Microsoft Agent Framework - Bootcamp Learning Plan

## Learning Path: Basic → Intermediate → Advanced

This bootcamp is structured as a step-by-step learning journey through the Microsoft Agent Framework (Python SDK). Each module builds on the previous one.

---

## Module Overview

| # | Module | Level | Topics |
|---|--------|-------|--------|
| 01 | Setup & Configuration | Basic | Environment, dependencies, providers, auth |
| 02 | Hello Agent | Basic | First agent, basic chat, ChatAgent, AzureOpenAIChatClient |
| 03 | Providers Deep Dive | Basic | AzureOpenAI, OpenAI, AzureAIAgentsProvider |
| 04 | Function Tools | Basic | @ai_function, custom tools, Annotated params |
| 05 | Conversation Threads | Basic | Multi-turn, thread persistence, context |
| 06 | Streaming Responses | Basic | run_stream, real-time output, async iteration |
| 07 | Structured Outputs | Intermediate | Pydantic response models, typed responses |
| 08 | Hosted Tools | Intermediate | CodeInterpreter, FileSearch, WebSearch |
| 09 | MCP Tools | Intermediate | HostedMCPTool, MCPStreamableHTTPTool |
| 10 | Middleware System | Intermediate | Agent-level, run-level, chat, function middleware |
| 11 | Workflows - Sequential | Intermediate | WorkflowBuilder, linear pipelines, edges |
| 12 | Workflows - Handoff | Intermediate | Conditional routing, triage, branching |
| 13 | Workflows - Concurrent | Intermediate | ConcurrentBuilder, parallel agents |
| 14 | Agent-as-Tool | Advanced | Hierarchical agents, as_tool() |
| 15 | Multi-Agent Supervisor | Advanced | Coordinator pattern, task delegation |
| 16 | Sub-Workflows | Advanced | Nested workflows, WorkflowExecutor |
| 17 | Human-in-the-Loop | Advanced | Approval gates, function invocation approval |
| 18 | Memory & Context | Advanced | ChatHistoryProviders, ContextProviders, sessions |
| 19 | Observability & Monitoring | Advanced | Tracing, logging, diagnostics |
| 20 | Declarative Agents | Advanced | YAML/config-driven agent definitions |
| 21 | Agent-to-Agent (A2A) | Advanced | A2A protocol, inter-agent communication |
| 22 | Deployment | Advanced | Azure Functions, containerized, production hosting |
| 23 | Capstone Project | Advanced | End-to-end multi-agent application |

---

## Prerequisites

- Python 3.13+
- Azure subscription (for Azure AI Foundry agents)
- Azure OpenAI resource OR OpenAI API key
- `uv` package manager (recommended)

## Quick Start

```bash
# Install dependencies
uv sync

# Set environment variables (see Module 01)
# Run any module
uv run python modules/01_setup_and_configuration/main.py
```

---

## Architecture Reference

```
User Query → Provider (AzureOpenAI / AzureAIAgents / OpenAI)
                ↓
            ChatAgent / create_agent()
                ↓
            Tools: Functions | Hosted (Code/Search/Web) | MCP
                ↓
            Middleware Pipeline (chat → function → agent)
                ↓
            Workflows: Sequential | Handoff | Concurrent | Sub-workflow
                ↓
            Response: Text | Structured (Pydantic) | Stream
```

## Key Imports Reference

```python
# Core
from agent_framework import ChatAgent, AgentRunContext, AgentRunResponse

# Providers
from agent_framework.azure import AzureOpenAIChatClient, AzureAIAgentsProvider
from agent_framework.openai import OpenAIChatClient

# Tools
from agent_framework import ai_function, HostedCodeInterpreterTool
from agent_framework import HostedFileSearchTool, HostedWebSearchTool
from agent_framework import HostedMCPTool, MCPStreamableHTTPTool

# Workflows
from agent_framework import WorkflowBuilder, WorkflowExecutor, Executor
from agent_framework import WorkflowContext, WorkflowEvent, handler
from agent_framework import ConcurrentBuilder

# Middleware
from agent_framework import AgentMiddleware, FunctionInvocationContext
from agent_framework import chat_middleware, function_middleware

# Auth
from azure.identity.aio import AzureCliCredential, DefaultAzureCredential
```
