# REQUIREMENTS.md

Derived from the official project spec (Modul 63184, Thema 4 — RAG-System,
Dr.-Ing. Otmane Azeroual, FernUniversität Hagen, SoSe 2026).

Each requirement maps to a testable acceptance criterion.
Status column is intentionally left for tracking: `[ ]` open · `[x]` done · `[~]` partial.

---

## 1. Dokumentenaufnahme (Document Ingestion)

| # | Requirement | Acceptance Criterion | Status |
|---|-------------|----------------------|--------|
| 1.1 | Upload PDF files | `POST /ingest` (or equivalent) accepts `.pdf` and returns a success response | `[ ]` |
| 1.2 | Upload DOCX files | Same endpoint accepts `.docx` | `[ ]` |
| 1.3 | Upload TXT files | Same endpoint accepts `.txt` | `[ ]` |
| 1.4 | Text extraction | Extracted text is non-empty and readable for all three formats | `[ ]` |
| 1.5 | Chunking | Documents are split into smaller segments; chunk size is configurable | `[ ]` |
| 1.6 | Metadata tagging | Each chunk stores `source` (filename), `page` number, and `title` | `[ ]` |

> **Current state:** `ingestion` service is a stub (`worker.py` heartbeat loop). `Chunk` schema in
> `shared/schemas.py` exists; `get_mock_chunks()` in `pipeline` is the placeholder.

---

## 2. Retrieval (Vector Search)

| # | Requirement | Acceptance Criterion | Status |
|---|-------------|----------------------|--------|
| 2.1 | Embedding generation | Each chunk is embedded via `nomic-embed-text` (already wired in `app/models.py`) | `[~]` |
| 2.2 | Vector storage | Embeddings are persisted in `pgvector` (`rag_postgres`) | `[ ]` |
| 2.3 | Metadata persistence | Chunk metadata (source, page, title) is stored alongside vectors | `[ ]` |
| 2.4 | Semantic search | Given a query, the top-N most similar chunks are returned via cosine similarity | `[ ]` |
| 2.5 | Replace mock chunks | `get_mock_chunks()` is replaced by a real DB lookup in `pipeline` | `[ ]` |

> **Current state:** retrieval is not yet implemented — `get_mock_chunks()` in `pipeline` returns
> placeholder data. `pgvector` is initialized via `infra/postgres/init.sql` but no vectors are being
> written or queried yet. Real retrieval logic will live inside `pipeline`, not a separate service.

---

## 3. Generative Answer (LLM Integration)

| # | Requirement | Acceptance Criterion | Status |
|---|-------------|----------------------|--------|
| 3.1 | Query → embedding | User query is embedded before retrieval (done in `evaluator.py`) | `[x]` |
| 3.2 | Similarity search | Retrieved chunks are ranked by similarity score | `[ ]` |
| 3.3 | Context aggregation | Top-N chunks are joined into a context string passed to the prompt builder | `[~]` |
| 3.4 | LLM response generation | `POST /augment` returns a non-empty `answer` for any in-domain query | `[x]` |
| 3.5 | Local model support | Works with `qwen2.5:1.5b` / `3b` / `7b` via Ollama (fast/complex modes) | `[x]` |
| 3.6 | API model support | Works with `provider="api"` (Gemini / Groq) via OpenAI-compatible endpoint | `[x]` |

---

## 4. Monitoring & Evaluation (LLM Safety + Quality)

| # | Requirement | Acceptance Criterion | Status |
|---|-------------|----------------------|--------|
| 4.1 | Structured answer | Response is coherent and addresses the user's question | `[~]` |
| 4.2 | Document-grounded answers | When context is available, answer does not introduce facts absent from chunks | `[ ]` |
| 4.3 | Source citation | `ChatResponse.sources` lists at least one `SourceReference` per answer | `[~]` |
| 4.4 | Out-of-domain guard | Queries with cosine similarity < 0.60 to domain topics are rejected gracefully | `[x]` |
| 4.5 | Hallucination mitigation | Prompt builder adds grounding instruction when Tavily fallback is used | `[x]` |
| 4.6 | Safety classifier | `llama-guard3:1b` judge zeroes unsafe responses and returns the hazard category | `[x]` |
| 4.7 | Prompt Engineering | At least 3 distinct roles (`technical`, `creative`, `concise`, etc.) are functional | `[x]` |
| 4.8 | Context size limiting | Compressor summarizes contexts > 1500 chars before generation | `[x]` |

---

## 5. Chat Interface

| # | Requirement | Acceptance Criterion | Status |
|---|-------------|----------------------|--------|
| 5.1 | Interactive chat UI | Streamlit frontend renders at `http://localhost:8501`; user can send a message | `[x]` |
| 5.2 | Source display | UI shows which documents/chunks were used in the answer | `[~]` |
| 5.3 | Query history | `views/history.py` displays past queries and responses | `[~]` |
| 5.4 | Confidence score | UI surfaces `ChatResponse.confidence` per answer | `[~]` |
| 5.5 | Docker-network routing | `BackendClient` targets service hostname (not `127.0.0.1`) when running in compose | `[ ]` |

> **Current state:** `BackendClient` hardcodes `http://127.0.0.1:8000` — breaks inside Docker compose
> network. Must be changed to `http://pipeline:8000` (or env-variable driven).

---

## 6. Evaluation (Deliverable)

| # | Requirement | Acceptance Criterion | Status |
|---|-------------|----------------------|--------|
| 6.1 | Answer quality report | Written evaluation of relevance and completeness across a test set | `[ ]` |
| 6.2 | Retrieval accuracy | Measured precision/recall of retrieved chunks vs. ground-truth answers | `[ ]` |
| 6.3 | Embedding model comparison | At least two embedding models benchmarked (e.g. `nomic-embed-text` vs. another) | `[ ]` |
| 6.4 | System performance | Latency and throughput measured under realistic load | `[ ]` |
| 6.5 | Chunk size comparison | (Optional) Evaluation across at least two chunk sizes | `[ ]` |
| 6.6 | Prompt strategy comparison | (Optional) Evaluation across at least two prompt roles/strategies | `[ ]` |

> No separate `generation` service exists anymore — `ragas`/`langgraph`/`tavily-python` would need
> to be added to `services/pipeline/pyproject.toml` if pursued for 6.1–6.2.

---

## 7. Infrastructure & Deployment

| # | Requirement | Acceptance Criterion | Status |
|---|-------------|----------------------|--------|
| 7.1 | Local dev via Docker Compose | `docker compose up -d --build` starts all services without manual steps | `[x]` |
| 7.2 | Demo mode (no host Ollama) | `docker-compose.demo.yml` overlay runs end-to-end on any machine | `[x]` |
| 7.3 | Cloud deployment | App runs on a cloud VM or container host | `[ ]` |
| 7.4 | Reverse proxy (NGINX) | NGINX terminates HTTPS and proxies to services | `[ ]` |
| 7.5 | HTTPS certificate | Let's Encrypt cert is configured and auto-renewing | `[ ]` |
| 7.6 | System architecture doc | Architecture diagram or written description is committed to the repo | `[ ]` |

---

## 8. Stub Services (to be implemented)

These services exist as heartbeat stubs and must be fully implemented:

| Service | Current state | Required |
|---------|--------------|---------|
| `ingestion` | `worker.py` loop | Implement document parsing, chunking, metadata tagging, embedding write to pgvector |

> Retrieval (vector similarity search, replacing `get_mock_chunks()`) and generation enhancements
> (e.g. LangGraph-based agentic generation, `ragas` evaluation) are no longer separate stub services —
> they're tracked as work items within `pipeline` under sections 2, 3, and 6 above.

---

## Quick Test Checklist

Run these manually (or automate) to verify core functionality end-to-end:

```bash
# 1. Stack starts cleanly
docker compose up -d --build
docker compose ps   # all services "Up"

# 2. Pipeline API responds
curl -s http://localhost:8000/augment \
  -H "Content-Type: application/json" \
  -d '{"query":"Was ist RAG?","settings":{"role":"technical","mode":"fast","provider":"local","max_tokens":512,"threshold":0.5}}' \
  | jq '.answer, .sources, .confidence'

# 3. Out-of-domain guard fires
curl -s http://localhost:8000/augment \
  -H "Content-Type: application/json" \
  -d '{"query":"Wie macht man Pasta?","settings":{"role":"concise","mode":"fast","provider":"local","max_tokens":256,"threshold":0.5}}' \
  | jq '.answer'   # should return "out of scope" message

# 4. Frontend reachable
curl -s -o /dev/null -w "%{http_code}" http://localhost:8501   # expect 200
```
