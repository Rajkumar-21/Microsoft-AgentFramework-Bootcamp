# Module 07: Structured Outputs

## Learning Objectives
- Use Pydantic models as `response_format` for typed responses
- Parse structured JSON from agent responses
- Design schemas for complex structured data

## Key Concepts
- **`response_format=PydanticModel`** - Force structured JSON output
- **`BaseModel`** with `ConfigDict(extra="forbid")` - Strict schema
- **`model_validate_json(result.text)`** - Parse response into model

## Exercises
1. Create a structured weather response model
2. Create a structured analysis report model
3. Handle validation errors gracefully

## Files
- `main.py` - Structured output examples with Pydantic
