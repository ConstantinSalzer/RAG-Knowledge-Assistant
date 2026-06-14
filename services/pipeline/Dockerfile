# docker image
FROM python:3.11-slim

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# set workdir and copy files
WORKDIR /app
COPY . .

# install dependencies
RUN uv pip install --system ./shared ./services/pipeline

# set environment variable for python path and workdir for the service
ENV PYTHONPATH=/app/services/pipeline
WORKDIR /app/services/pipeline

# run the service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]