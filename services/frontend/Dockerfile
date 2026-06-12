# Use the official uv image to grab the binary
FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# 1. Copy workspace configuration and shared library
# This allows uv to resolve the 'shared' dependency correctly
COPY pyproject.toml uv.lock /app/
COPY shared/ /app/shared/

# 2. Copy the frontend service code
COPY services/frontend/ /app/services/frontend/

# 3. Install everything using uv
# --system installs into the container's python environment
# We install the shared lib and the frontend app together
RUN uv pip install --system ./shared ./services/frontend

# Change to the service directory for execution
WORKDIR /app/services/frontend

EXPOSE 8501

# Start streamlit
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
