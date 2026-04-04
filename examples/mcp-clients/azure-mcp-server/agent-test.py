"""
# create agent that uses mcp tools from tool/azuremcp-client-tool.py to connect to azure mcp server and run a query
"""
import asyncio
import os
from agent_framework.openai import OpenAIChatClient


client = OpenAIChatClient(
    model=os.environ["AZURE_OPENAI_MODEL"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"]
)

