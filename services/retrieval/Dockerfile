FROM python:3.12-slim

WORKDIR /app

COPY services/retrieval/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt python-multipart

COPY services/retrieval/app ./app
COPY services/retrieval/main.py ./main.py
COPY services/retrieval/ingest_routes.py ./ingest_routes.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
