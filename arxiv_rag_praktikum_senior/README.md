# arXiv RAG Praktikumsprojekt

Kompaktes RAG-System für eine Praktikumsarbeit.

## Umfang

Das Projekt enthält:

- arXiv-Crawler per CLI
- einfache Paper-Bewertung über Schlagwörter
- Duplikaterkennung
- PDF-Download mit 5-Sekunden-Abstand
- PDF-Text-Extraktion
- Chunking
- Embedding-Erzeugung
- Speicherung in PostgreSQL mit pgvector
- semantisches Retrieval über FastAPI

Bewusst nicht enthalten:

- Web-Oberfläche
- Frontend

## Architektur

```text
CLI
 ├── crawl
 ├── download
 └── ingest

FastAPI
 ├── GET  /health
 └── POST /search
```

Crawler, Download und Ingest laufen bewusst über die Kommandozeile.
Die FastAPI-Anwendung stellt nur die Retrieval-Schnittstelle bereit.

## Start

```bash
cp .env.example .env
docker compose up -d

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python -m app.cli init
python -m app.cli crawl --query "retrieval augmented generation" --max-results 20
python -m app.cli download
python -m app.cli ingest
```

## Retrieval-API starten

```bash
uvicorn app.api.main:app --reload
```

## Suche

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query":"hybrid retrieval rag", "limit":5}'
```

## Tests

```bash
pytest
```
