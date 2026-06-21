"""Azure Functions host for Commerce Concierge.

Exposes the concierge workflow as an HTTP-triggered agent:
    POST /api/agents/CommerceConcierge/run

Deploy:
    pip install agent-framework-azurefunctions --pre
    func azure functionapp publish <your-function-app>
"""

from __future__ import annotations

import asyncio

from agent_framework.azure import AgentFunctionApp

from .workflow import build_concierge_workflow

_workflow = asyncio.run(build_concierge_workflow())
_concierge = _workflow.as_agent(name="CommerceConcierge")

app = AgentFunctionApp(agents=[_concierge])
