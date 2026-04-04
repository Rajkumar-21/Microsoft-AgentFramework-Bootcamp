FROM python:3.13-slim

WORKDIR /app

# Install uv for fast dependency management
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY modules/ modules/

# Install dependencies
RUN uv sync --no-dev

# Set default module to run (override with docker run command)
CMD ["uv", "run", "python", "modules/22_deployment/main.py"]
