import os
import time
import logging
import requests
from typing import Any, List

logger = logging.getLogger(__name__)

MODEL_REGISTRY = {
    "summarizer": {
        "fast": os.getenv("MODEL_SUMMARIZER_FAST"),
        "complex": os.getenv("MODEL_SUMMARIZER_COMPLEX"),
    },
    "judge": os.getenv("MODEL_JUDGE"),
    "generator": {
        "fast": os.getenv("MODEL_GENERATOR_FAST"),
        "complex": os.getenv("MODEL_GENERATOR_COMPLEX"),
    },
}

def call_model(task: str, prompt: str, max_tokens: int, stream: bool = False, mode: str = "fast") -> Any:

    # generator is mode-dependent: fast vs complex
    model_entry = MODEL_REGISTRY.get(task)
    model_name = model_entry.get(mode, model_entry["fast"]) if isinstance(model_entry, dict) else model_entry
    url = os.getenv('OLLAMA_URL')

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": stream,
        "options": {"num_predict": max_tokens}
    }

    logger.info(f"[LLM IN] task={task} model={model_name} max_tokens={max_tokens} prompt={prompt!r}")

    # generous timeout: CPU inference for larger models (e.g. qwen2.5:7b) can take well over 60s
    call_start = time.time()
    response = requests.post(url, json=payload, stream=stream, timeout=300)

    response.raise_for_status()

    if not stream:
        result = response.json().get("response", "").strip()
        logger.info(f"[TIMER] call_model task={task} model={model_name} (models.py): {time.time() - call_start:.3f}s")
        logger.info(f"[LLM OUT] task={task} model={model_name} response={result!r}")
        return result

    logger.info(f"[TIMER] call_model task={task} model={model_name} (models.py, stream init): {time.time() - call_start:.3f}s")
    return response

def get_embedding(text: str) -> List[float]:

    # derive the embeddings endpoint from OLLAMA_URL (.../api/generate -> .../api/embeddings)
    url = os.getenv('OLLAMA_URL').replace('/api/generate', '/api/embeddings')
    model_name = os.getenv('EMBEDDING_MODEL')

    payload = {"model": model_name, "prompt": text}

    call_start = time.time()
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    logger.info(f"[TIMER] get_embedding model={model_name} (models.py): {time.time() - call_start:.3f}s")

    return response.json().get("embedding", [])