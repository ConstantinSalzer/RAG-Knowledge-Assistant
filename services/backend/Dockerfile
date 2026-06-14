# docker image
FROM python:3.11-slim

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# set workdir and copy files
WORKDIR /app
COPY . .

# install dependencies
RUN uv pip install --system ./shared ./services/backend

EXPOSE 8000

# run the service (module paths are rooted at /app, e.g. services.backend.main)
CMD ["python", "-m", "uvicorn", "services.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
