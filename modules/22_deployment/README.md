# Module 22: Deployment

## Learning Objectives
- Deploy agents to Azure (Azure Functions, Container Apps, App Service)
- Package agents for production deployment
- Configure authentication for deployed agents
- Set up monitoring and scaling

## Key Concepts
- **Azure Functions** - Serverless agent hosting
- **Container Apps** - Containerized agent deployment
- **Production auth** - `DefaultAzureCredential` for managed identity
- **Environment configuration** - Azure App Settings for secrets
- **Scaling** - Auto-scaling for agent workloads

## Deployment Options

| Option | Best For | Scaling |
|--------|----------|---------|
| Azure Functions | Event-driven agents | Auto-scale |
| Container Apps | Long-running agents | KEDA-based |
| App Service | Web-exposed agents | Manual/auto |
| AKS | Complex multi-agent | Kubernetes |

## Exercises
1. Create a Dockerfile for agent deployment
2. Set up Azure Function for an agent endpoint
3. Configure production authentication with managed identity
4. Set up health checks and monitoring

## Files
- `Dockerfile` - Container deployment configuration
- `function_app.py` - Azure Functions agent example
- `main.py` - Production deployment patterns
