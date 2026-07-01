# Module 04: Function Tools

> **Scenario — Lakeside Outfitters Order Operations Agent.** A support agent that
> resolves real requests — order status, stock checks, delivery ETAs, and refunds —
> by calling typed Python functions the model invokes on demand (and chains together).

## Learning Objectives
- Create custom function tools for agents
- Use type hints + `Annotated[type, Field(description=...)]` for parameters
- Pass plain functions directly to the `tools=[]` parameter
- Understand auto-conversion of Python functions to AI-callable tools

## Key Concepts
- **Plain functions as tools** - no decorator required; pass them in `tools=[...]`
- **`Annotated[str, Field(description=...)]`** - typed parameters with descriptions
- **Docstrings** - used as the tool description by the framework
- **Tools as a trust boundary** - validate and authorize inside the function

## Exercises
1. Add a `track_shipment` tool that returns a carrier + tracking number
2. Make `initiate_refund` require an order in a refundable state
3. Observe the agent chaining `lookup_order_status` + `estimate_delivery`
4. Add audit logging inside `initiate_refund`

## How to Run
```bash
cd modules/04_function_tools
python main.py
```

## Files
- `main.py` - Order operations agent with four typed tools
