import asyncio
import os
from azure_openai_config import get_azure_chat_service, AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME, AZURE_OPENAI_API_VERSION


async def main():
    print("=== Azure OpenAI Configuration Validation ===")
    
    # Check environment variables first
    print("\nEnvironment Variables:")
    print(f"AZURE_OPENAI_API_KEY: {'Set' if AZURE_OPENAI_API_KEY else 'Not Set'}")
    print(f"AZURE_OPENAI_ENDPOINT: {AZURE_OPENAI_ENDPOINT if AZURE_OPENAI_ENDPOINT else 'Not Set'}")
    print(f"AZURE_OPENAI_DEPLOYMENT_NAME: {AZURE_OPENAI_DEPLOYMENT_NAME if AZURE_OPENAI_DEPLOYMENT_NAME else 'Not Set'}")
    print(f"AZURE_OPENAI_API_VERSION: {AZURE_OPENAI_API_VERSION if AZURE_OPENAI_API_VERSION else 'Not Set'}")
    
    # Check for missing required variables
    missing_vars = []
    if not AZURE_OPENAI_API_KEY:
        missing_vars.append("AZURE_OPENAI_API_KEY")
    if not AZURE_OPENAI_ENDPOINT:
        missing_vars.append("AZURE_OPENAI_ENDPOINT")
    if not AZURE_OPENAI_DEPLOYMENT_NAME:
        missing_vars.append("AZURE_OPENAI_DEPLOYMENT_NAME")
    if not AZURE_OPENAI_API_VERSION:
        missing_vars.append("AZURE_OPENAI_API_VERSION")
    
    if missing_vars:
        print(f"\nERROR: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file and ensure all required variables are set.")
        return
    
    # Try to create the chat client
    try:
        chat_client = get_azure_chat_service()
        print("\n✅ Azure OpenAI Chat Client created successfully!")
        
        # Test a simple connection (this will help identify connection issues)
        print("\nTesting connection...")
        test_agent = chat_client.create_agent(
            name="TestAgent",
            instructions="You are a test agent. Respond with 'Connection successful!' when prompted."
        )
        
        # Simple test query
        result = await test_agent.run("Test connection")
        print("✅ Connection test successful!")
        print(f"Response: {result.text}")
        
    except Exception as e:
        print(f"\n❌ Error creating or testing Azure OpenAI Chat Client: {e}")
        print("\nTroubleshooting tips:")
        print("1. Verify your Azure OpenAI endpoint is correct")
        print("2. Check that your API key is valid")
        print("3. Ensure your deployment name exists in your Azure OpenAI resource")
        print("4. Verify network connectivity to the endpoint")


if __name__ == "__main__":
    asyncio.run(main())