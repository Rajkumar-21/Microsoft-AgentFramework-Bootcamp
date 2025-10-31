# Simple test workflow to check devui input behavior
# pip install agent-framework-devui==1.0.0b251016

import os
import sys
import logging
from dotenv import load_dotenv

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Use a proper logger
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

from agent_framework import WorkflowBuilder
from config.azure_openai_config import get_azure_chat_service

# Configure environment
load_dotenv(override=True)

# Initialize chat client
chat_client = get_azure_chat_service()

# Create a simple echo agent
echo_agent = chat_client.create_agent(
    instructions=(
        "You are a simple echo agent. "
        "Repeat back what the user said, but add 'Echo: ' at the beginning. "
        "If the user input is empty or unclear, ask them to provide input."
    ),
    name="echo_agent",
)

# Build simple workflow
workflow = (
    WorkflowBuilder()
    .set_start_executor(echo_agent)
    .build()
)

def main():
    from agent_framework.devui import serve
    
    serve(entities=[workflow], port=8096, auto_open=True)

if __name__ == "__main__":
    main()