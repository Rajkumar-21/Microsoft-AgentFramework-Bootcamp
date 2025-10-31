# Copyright (c) Microsoft. All rights reserved.
# pip install agent-framework-devui==1.0.0b251016

import os
import sys
import logging
from typing import Any

from agent_framework import AgentExecutorResponse, WorkflowBuilder
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Annotated

# Add the project root directory to Python path if needed (your project layout)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Use a proper logger
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Use whatever chat client factory you already have in your project
from config.azure_openai_config import get_azure_chat_service
from dotenv import load_dotenv

# Configure OpenAI client based on environment
load_dotenv(override=True)

"""
Sample: Sequential workflow with user input processing using devui

This workflow accepts user input, processes it through a writer agent, 
then reviews and finalizes it through a reviewer agent.

Flow: User Input → Writer Agent → Reviewer Agent → Final Output

The workflow can be visualized and executed through the devui interface.
You can provide any type of content request as input.

Prerequisites:
- Azure OpenAI access configured for AzureOpenAIChatClient (use az login + env vars)
- agent-framework-devui package installed

Usage:
1. Run this script to start the devui server
2. Open the web interface (automatically opens in browser)
3. Input your content request (e.g., "Write a blog post about AI", "Create a product description for wireless headphones")
4. Watch the workflow execute: Writer creates content → Reviewer polishes it → Final result
"""

# Initialize chat client
chat_client = get_azure_chat_service()

# Create Writer agent - generates content based on user input
writer = chat_client.create_agent(
    instructions=(
        "You are an excellent content writer. "
        "Create clear, engaging content based on the user's request. "
        "Focus on clarity, accuracy, and proper structure. "
        "Provide comprehensive content that fully addresses the user's input."
    ),
    name="writer",
)

# Create Reviewer agent - reviews and provides final polished version
reviewer = chat_client.create_agent(
    instructions=(
        "You are a thoughtful reviewer and editor. "
        "Review the writer's content and provide a final, polished version. "
        "Improve clarity, fix any issues, and ensure the content is well-structured. "
        "Provide the final version that is ready for publication."
    ),
    name="reviewer",
)

# Build sequential workflow using WorkflowBuilder: writer -> reviewer
workflow = (
    WorkflowBuilder()
    .set_start_executor(writer)
    .add_edge(writer, reviewer)
    .build()
)


def main():
    from agent_framework.devui import serve

    serve(entities=[workflow], port=8094, auto_open=True)


if __name__ == "__main__":
    main()