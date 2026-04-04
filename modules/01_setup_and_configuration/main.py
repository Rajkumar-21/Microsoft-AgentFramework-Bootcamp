"""
Module 01: Setup & Configuration
Validates that your environment is properly configured for the Agent Framework.
"""

import os
import sys


def validate_config():
    """Check required environment variables are set."""
    required_vars = {
        "AZURE_OPENAI_ENDPOINT": "Azure OpenAI endpoint URL (e.g., https://myresource.openai.azure.com)",
        "AZURE_OPENAI_API_KEY": "Azure OpenAI API key",
        "AZURE_OPENAI_MODEL": "Model deployment name (e.g., gpt-4o-mini)",
    }

    optional_vars = {
        "FOUNDRY_PROJECT_ENDPOINT": "Azure AI Foundry project endpoint (e.g., https://myproject.services.ai.azure.com)",
        "FOUNDRY_MODEL": "Azure AI Foundry model deployment name",
        "OPENAI_API_KEY": "OpenAI API key (for direct OpenAI provider)",
    }

    print("=" * 60)
    print("Microsoft Agent Framework - Configuration Validator")
    print("=" * 60)

    # Check required
    missing = []
    print("\n✅ Required Environment Variables:")
    for var, desc in required_vars.items():
        value = os.environ.get(var)
        if value:
            masked = value[:8] + "..." if len(value) > 8 else "***"
            print(f"  ✓ {var} = {masked}")
        else:
            print(f"  ✗ {var} - MISSING ({desc})")
            missing.append(var)

    # Check optional
    print("\n📋 Optional Environment Variables:")
    for var, desc in optional_vars.items():
        value = os.environ.get(var)
        if value:
            masked = value[:8] + "..." if len(value) > 8 else "***"
            print(f"  ✓ {var} = {masked}")
        else:
            print(f"  ○ {var} - Not set ({desc})")

    # Check agent-framework package
    print("\n📦 Package Check:")
    try:
        import agent_framework

        print(f"  ✓ agent-framework {agent_framework.__version__} installed")
    except ImportError:
        print("  ✗ agent-framework NOT installed")
        print("    Run: uv add agent-framework")
        missing.append("agent-framework package")

    # Summary
    print("\n" + "=" * 60)
    if missing:
        print(f"⚠️  {len(missing)} issue(s) found. Fix them before proceeding.")
        sys.exit(1)
    else:
        print("✅ All required configurations are set. Ready to go!")


if __name__ == "__main__":
    validate_config()
