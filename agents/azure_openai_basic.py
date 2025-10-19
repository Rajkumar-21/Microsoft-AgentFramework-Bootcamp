import asyncio
import sys
import os
import logging
# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.azure_openai_config import get_azure_chat_service
from agent_framework.azure import AzureOpenAIChatClient
from tools.functions.time import get_time
# Validate environment before creating the client
chat_client = get_azure_chat_service()
logging.info(f"Loaded Openai service: {chat_client.endpoint}")

agent = chat_client.create_agent(
    name="HelpDeskAgent",
    description="You are helpfull assitant",
    instructions="Always guide user to route it to respective team based on user queries.",
    tools=[get_time]
)


 
async def main():  
    # Create a thread to hold the conversation  
    # If no thread is provided, a new thread will be  
    # created and returned with the initial response  
    thread = agent.get_new_thread()
      
    print("Chat started! Type 'quit', 'end', or 'exit' to end the conversation.")  
      
    try:  
        while True:  
            user_input = input("\nUser: ")  
              
            # Check for exit conditions  
            if user_input.lower().strip() in ['quit', 'end', 'exit']:  
                print("Ending conversation...")  
                break  
              
            if not user_input.strip():  
                continue  
              
            print("Assistant: ", end="", flush=True)  
              
            # Stream the response and maintain thread context  
            result = await agent.run(messages=user_input, thread=thread)
            print(result.text, end="", flush=True)  
              
            print()  # New line after response  
              
    except (KeyboardInterrupt, EOFError):  
        print("\n\nConversation interrupted by user.")  

  
if __name__ == "__main__":  
    asyncio.run(main())