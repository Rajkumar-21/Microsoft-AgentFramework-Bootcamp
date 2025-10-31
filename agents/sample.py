import asyncio
from typing import Annotated
from pydantic import Field
import os,sys# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Agent Framework imports
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
from config.azure_openai_config import get_azure_chat_service
chat_client = get_azure_chat_service()
# --- Tools (migrated from MenuPlugin methods) ---
def get_specials() -> str:
    """
    Replaces MenuPlugin.get_specials()
    Tool functions are regular callables in Agent Framework.
    We log invocation so you can observe 'function call' behavior.
    """
    specials = """
    Special Soup: Clam Chowder
    Special Salad: Cobb Salad
    Special Drink: Chai Tea
    """
    print("[Tool] get_specials called -> returning specials")
    return specials


def get_item_price(
    menu_item: Annotated[str, Field(description="The name of the menu item.")]
) -> str:
    """
    Replaces MenuPlugin.get_item_price(menu_item)
    Note: Agent Framework will call this function when the LLM decides to invoke it.
    """
    print(f"[Tool] get_item_price called with menu_item={menu_item!r} -> returning price")
    return "$9.99"


# --- Example migration of interaction loop ---
async def main() -> None:
    # Create the ChatAgent using the Azure Chat client (similar to AzureChatCompletion in SK)
    # For auth, run `az login` first or use another credential strategy
    chat_client = get_azure_chat_service()

    # Create the agent and register tools at agent-level
    agent = ChatAgent(
        chat_client=chat_client,
        instructions="Answer questions about the menu.",
        tools=[get_specials, get_item_price],  # tools available to the agent
    )

    user_inputs = [
        "Hello",
        "What is the special soup?",
        "How much does that cost?",
        "Thank you",
    ]

    # Use the same agent instance across turns so conversation context is preserved.
    # We'll use streaming to surface intermediate generation as it happens.
    for user_input in user_inputs:
        print(f"\n# User: '{user_input}'")
        # Stream the agent's response (prints chunks as they arrive)
        # During generation, if the model triggers a function/tool call,
        # the Agent Framework will execute the corresponding Python callable (our tool),
        # and the tool's print statements will show that activity.
        print("# Agent (streaming): ", end="", flush=True)
        async for chunk in agent.run_stream(user_input):
            # chunk.text holds incremental text content; print as it arrives.
            if getattr(chunk, "text", None):
                print(chunk.text, end="", flush=True)
        print()  # newline after streaming finishes

    print("\n=== Conversation finished ===")


if __name__ == "__main__":
    asyncio.run(main())