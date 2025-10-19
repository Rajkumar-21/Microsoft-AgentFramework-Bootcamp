import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.azure_openai_config import get_azure_chat_service


# Validate environment before creating the client
chat_client = get_azure_chat_service()

def validate(chat_client) -> tuple[bool, list[str]]:
        """Validate configuration settings"""
        errors = []
        
        # Basic validation that the chat client exists
        if not chat_client:
            errors.append("Chat client is not initialized")
            return False, errors
            
        # Check if the client has the necessary configuration
        try:
            # The client should be configured and ready to use
            if not hasattr(chat_client, '_client'):
                errors.append("Chat client is not properly initialized")
            
            # Get configuration details from the environment
            from config.azure_openai_config import (
                AZURE_OPENAI_API_KEY,
                AZURE_OPENAI_ENDPOINT,
                AZURE_OPENAI_DEPLOYMENT_NAME,
                AZURE_OPENAI_MODEL_NAME,
                AZURE_OPENAI_API_VERSION
            )
            
            # Print configuration details with masked API key
            print("\n🔐 Azure OpenAI Configuration Details:")
            print("-" * 50)
            
            # Mask API key - show first 2 and last 2 characters
            if AZURE_OPENAI_API_KEY:
                masked_key = f"{AZURE_OPENAI_API_KEY[:2]}{'*' * (len(AZURE_OPENAI_API_KEY)-4)}{AZURE_OPENAI_API_KEY[-2:]}"
                print(f"API Key       : {masked_key}")
            else:
                print("API Key       : ❌ Not set")
            
            print(f"Endpoint      : {AZURE_OPENAI_ENDPOINT or '❌ Not set'}")
            print(f"Model         : {AZURE_OPENAI_MODEL_NAME or '❌ Not set'}")
            print(f"Deployment    : {AZURE_OPENAI_DEPLOYMENT_NAME or '❌ Not set'}")
            print(f"API Version   : {AZURE_OPENAI_API_VERSION or '❌ Not set'}")
            print("-" * 50)
            
            # Validate required configurations
            if not AZURE_OPENAI_API_KEY:
                errors.append("Azure OpenAI API key is not set")
            if not AZURE_OPENAI_ENDPOINT:
                errors.append("Azure OpenAI endpoint is not set")
            if not AZURE_OPENAI_MODEL_NAME:
                errors.append("Azure OpenAI model name is not set")
            if not AZURE_OPENAI_DEPLOYMENT_NAME:
                errors.append("Azure OpenAI deployment name is not set")
            
            # If we have a client and no errors, it's valid
            return len(errors) == 0, errors
            
        except Exception as e:
            errors.append(f"Error validating chat client: {str(e)}")
            return False, errors

print("Validating Azure OpenAI Chat Client configuration...")
is_valid, validation_errors = validate(chat_client)

# if is_valid:
#     print("Azure OpenAI Chat Client configuration is valid.")
# else:
#     print("Azure OpenAI Chat Client configuration is invalid:")
#     for error in validation_errors:
#         print(f" - {error}")