# Module 04: Function Tools

## Learning Objectives
- Create custom function tools for agents
- Use `@ai_function` decorator and `Annotated[type, Field()]` for parameters
- Pass functions directly to `tools=[]` parameter
- Understand auto-conversion of Python functions to AI-callable tools

## Key Concepts
- **`@ai_function`** - Decorator to mark functions as agent tools
- **`Annotated[str, Field(description=...)]`** - Typed parameters with descriptions
- **Docstrings** - Used as tool descriptions by the framework
- **Return values** - String responses back to the agent

## Exercises
1. Create a weather lookup tool
2. Create a time/date tool  
3. Create a calculator tool
4. Combine multiple tools in one agent
5. Observe how the agent decides which tool to call

## Files
- `main.py` - Agent with multiple function tools
