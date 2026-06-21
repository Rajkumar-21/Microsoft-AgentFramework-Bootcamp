"""Azure Functions host for Ops Copilot.

Exposes the incident workflow as an HTTP-triggered agent:
    POST /api/agents/OpsCopilot/run

Deploy:
    pip install agent-framework-azurefunctions --pre
    func azure functionapp publish <your-function-app>
"""

from __future__ import annotations

import asyncio

from agent_framework.azure import AgentFunctionApp

from .workflow import build_incident_workflow

# Build the workflow once at cold start and expose it as a single agent.
_workflow = asyncio.run(build_incident_workflow())
_ops_copilot = _workflow.as_agent(name="OpsCopilot")

app = AgentFunctionApp(agents=[_ops_copilot])
