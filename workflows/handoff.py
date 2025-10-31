# Copyright (c) Microsoft. All rights reserved.
# pip install agent-framework-devui==1.0.0b251016

import os
import sys
import logging
from typing import Any

from agent_framework import (
    ChatAgent,
    WorkflowBuilder,
    AgentExecutorResponse,
)
from dotenv import load_dotenv
from pydantic import BaseModel

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Use a proper logger
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

from config.azure_openai_config import get_azure_chat_service

# Configure OpenAI client based on environment
load_dotenv(override=True)

"""
Sample: Customer Support Handoff Workflow using WorkflowBuilder and devui

This workflow demonstrates a customer support scenario where a triage agent 
routes requests to specialized agents based on the customer's needs.

Flow: User Input → Triage Agent → Specialist Agent → Final Response

The workflow includes:
- Triage agent that analyzes customer requests
- Refund specialist for refund-related issues  
- Order specialist for shipping/delivery issues
- General support agent for other concerns

Prerequisites:
- Azure OpenAI access configured
- agent-framework-devui package installed

Usage:
1. Run this script to start the devui server
2. Open the web interface 
3. Input customer support requests (e.g., "I need a refund", "My package is late", "I have a question")
4. Watch the workflow route to appropriate specialists
"""

# Initialize chat client
chat_client = get_azure_chat_service()

# Define structured output for triage decisions
class TriageDecision(BaseModel):
    """Triage decision with routing information."""
    
    department: str  # "refund", "order", or "support"
    reasoning: str   # Why this department was chosen
    initial_response: str  # Initial response to customer

# Condition function: route to refund if department is "refund"
def needs_refund_help(message: Any) -> bool:
    """Check if triage decided to route to refund department."""
    if not hasattr(message, 'agent_run_response'):
        return False
    try:
        decision = TriageDecision.model_validate_json(message.agent_run_response.text)
        return decision.department.lower() == "refund"
    except Exception:
        # Fallback to text analysis if structured response fails
        if hasattr(message.agent_run_response, 'text'):
            text = message.agent_run_response.text.lower()
            return 'refund' in text or 'return' in text or 'money back' in text
        return False

# Condition function: route to order if department is "order"
def needs_order_help(message: Any) -> bool:
    """Check if triage decided to route to order department."""
    if not hasattr(message, 'agent_run_response'):
        return False
    try:
        decision = TriageDecision.model_validate_json(message.agent_run_response.text)
        return decision.department.lower() == "order"
    except Exception:
        # Fallback to text analysis if structured response fails
        if hasattr(message.agent_run_response, 'text'):
            text = message.agent_run_response.text.lower()
            return any(word in text for word in ['shipping', 'delivery', 'order', 'package', 'tracking'])
        return False

# Condition function: route to support for all other cases
def needs_general_support(message: Any) -> bool:
    """Check if triage decided to route to general support."""
    if not hasattr(message, 'agent_run_response'):
        return True
    try:
        decision = TriageDecision.model_validate_json(message.agent_run_response.text)
        return decision.department.lower() == "support"
    except Exception:
        # If structured response fails, route to support if not refund or order
        return not needs_refund_help(message) and not needs_order_help(message)

# Create Triage agent - analyzes requests and determines routing with structured output
triage = chat_client.create_agent(
    instructions=(
        "You are a customer support triage agent. \n\n"
        "IMPORTANT: Check if you received actual customer input or if the input is empty/missing.\n\n"
        "If the input is empty, null, or just whitespace, respond with:\n"
        "{\n"
        "  \"department\": \"support\",\n"
        "  \"reasoning\": \"No customer request provided. Waiting for user input.\",\n"
        "  \"initial_response\": \"Welcome to customer support! Please describe what you need help with today. You can ask about refunds, order tracking, or any other questions.\"\n"
        "}\n\n"
        "If you receive a valid customer request, analyze it and determine the appropriate department:\n"
        "- department: 'refund' for refund/return requests, 'order' for shipping/delivery issues, 'support' for other inquiries\n"
        "- reasoning: brief explanation of why you chose this department\n"
        "- initial_response: helpful initial response to the customer\n\n"
        "Example customer requests:\n"
        "- 'I want to return my order' → refund department\n"
        "- 'Where is my package?' → order department\n"
        "- 'I can't log into my account' → support department"
    ),
    name="triage_agent",
    response_format=TriageDecision,
)

# Create Refund specialist
refund_agent = chat_client.create_agent(
    instructions=(
        "You are a refund specialist. Help customers with refund and return requests. "
        "Ask for order details, explain the refund process, and provide clear next steps. "
        "Be empathetic and ensure customers understand the timeline and requirements."
    ),
    name="refund_agent",
)

# Create Order/Shipping specialist  
order_agent = chat_client.create_agent(
    instructions=(
        "You are an order and shipping specialist. Help customers with delivery issues, "
        "tracking problems, and order status inquiries. Ask for order numbers when needed "
        "and provide detailed tracking assistance and delivery solutions."
    ),
    name="order_agent",
)

# Create General support agent
support_agent = chat_client.create_agent(
    instructions=(
        "You are a general customer support agent. Help customers with various inquiries "
        "that don't fall into refunds or shipping categories. Provide helpful troubleshooting, "
        "product information, account assistance, and gather necessary details to resolve issues."
    ),
    name="support_agent",
)

# Create Final Response agent - provides closure and summary
final_response_agent = chat_client.create_agent(
    instructions=(
        "You are a customer service completion agent. Review the specialist's response and provide a final, "
        "professional closure to the customer interaction. Include:\n"
        "1. A brief acknowledgment of the issue addressed\n"
        "2. Summary of the solution or next steps provided\n"
        "3. Professional closing with offers for further assistance\n"
        "Keep it concise but warm and professional."
    ),
    name="final_response_agent",
)

# Build the handoff workflow using WorkflowBuilder
# This creates a branching workflow where triage routes to different specialists,
# and all specialists converge to a final response agent
workflow = (
    WorkflowBuilder()
    .set_start_executor(triage)
    # Branch to different specialists based on triage decision
    .add_edge(triage, refund_agent, condition=needs_refund_help)
    .add_edge(triage, order_agent, condition=needs_order_help) 
    .add_edge(triage, support_agent, condition=needs_general_support)
    # All specialists converge to final response agent
    .add_edge(refund_agent, final_response_agent)
    .add_edge(order_agent, final_response_agent)
    .add_edge(support_agent, final_response_agent)
    .build()
)

def main():
    from agent_framework.devui import serve
    
    serve(entities=[workflow], port=8095, auto_open=True)

if __name__ == "__main__":
    main()