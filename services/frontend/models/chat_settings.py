from dataclasses import dataclass


@dataclass
class ChatSettings:

    top_k: int = 5
    llm: str = "GPT-4"
    prompting_strategy: str = "Standard RAG"

    MIN_TOP_K = 1
    MAX_TOP_K = 20

    LLM_OPTIONS = ["GPT-4", "Llama 3", "Mistral"]
    PROMPT_STRATEGIES = ["Standard RAG", "Chain of Thought", "Concise"]