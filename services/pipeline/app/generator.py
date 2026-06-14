import os
import requests
from typing import Any

from app.models import call_model

def get_llm_response(prompt: str, provider: str, max_tokens: int, mode: str = "fast", stream: bool = False) -> Any:

    if provider.lower() == "local":
        return call_model(
            task="generator",
            prompt=prompt,
            max_tokens=max_tokens,
            stream=stream,
            mode=mode
        )

    else:
        url, payload, headers = _prepare_api_request(prompt, max_tokens, stream)

        response = requests.post(url, json=payload, headers=headers, stream=stream, timeout=60)
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

def _prepare_api_request(prompt: str, max_tokens: int, stream: bool = False):

    # provider-agnostic, OpenAI-compatible chat-completions endpoint
    provider = os.getenv("API_PROVIDER", "gemini")
    api_key = os.getenv("API_KEY")
    url = os.getenv("API_BASE_URL")
    model = os.getenv("API_MODEL")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "stream": stream,
    }

    # Gemini-specific: disable "thinking" tokens so max_tokens is fully available for the answer
    if provider.lower() == "gemini":
        payload["extra_body"] = {"google": {"thinking_config": {"thinking_budget": 0}}}

    return url, payload, headers